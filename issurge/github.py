import json
from functools import cache
from itertools import chain
from typing import Any, Literal, NamedTuple

from rich import print

from issurge.utils import run


class OwnerInfo(NamedTuple):
    in_organization: bool
    owner: str
    repo: str

    def __rich_repr__(self):
        yield "in_org", self.in_organization, False
        yield "owner", self.owner, ""
        yield "repo", self.repo, ""


@cache
def repo_info():
    response = json.loads(
        run(
            ["gh", "repo", "view", "--json", "isInOrganization,owner,name"],
            bypass_dry_run=True,
        )
        or "{}"
    )
    return OwnerInfo(
        in_organization=response["isInOrganization"],
        owner=response["owner"]["login"],
        repo=response["name"],
    )


@cache
def available_issue_types() -> list[str]:
    repo = repo_info()

    if not repo.in_organization:
        return []

    return json.loads(
        call_api(
            "GET",
            f"/orgs/{repo.owner}/issue-types",
            jq="[ .[].name ]",
            bypass_dry_run=True,
        )
        or "[]"
    )


type IssueFieldType = Literal["number", "single_select", "text", "date"]


class IssueField(NamedTuple):
    name: str
    id: int
    type: IssueFieldType
    options: list[str]

    def normalize_value(self, val: Any) -> Any:
        """
        Handles casing differences & whitespace stripping
        for enum-type data
        """

        if self.type != "single_select":
            return val

        # Did you say POTENTIAL??
        for potential in self.options:
            if potential.lower() == str(val).lower().strip():
                return potential

        raise KeyError(
            f"{val!r} does not match any option for field {self.name!r} ({self.id}): "
            f"options are {', '.join(self.options)}"
        )


@cache
def available_issue_fields() -> list[IssueField]:
    repo = repo_info()

    if not repo.in_organization:
        return []

    fields = json.loads(
        call_api(
            "GET",
            f"/orgs/{repo.owner}/issue-fields",
            jq="""
                
                [
                
                .[] | {
                    id: .id,
                    name: .name,
                    type: .data_type,
                    options: [
                        (.options // [])[].name
                    ] 
                }

                ]
                
            """.replace("\n", "").strip(),
            bypass_dry_run=True,
        )
        or "{}"
    )

    return [IssueField(**field) for field in fields]


@cache
def available_issue_field_shorthands() -> dict[str, tuple[IssueField, str]]:
    """
    Returns a dict mapping shorthands (without the : prefix)
    to their corresponding field(id)+value
    """

    def into_shorthand(option: str):
        return option.replace(" ", "_")

    all_fields = available_issue_fields()
    # TODO: use [ *i for i in a ] once Python 3.15 is released
    all_enum_values = [
        into_shorthand(option) for field in all_fields for option in field.options
    ]

    # TODO: maybe we can avoid the loop + variable altogether once we have
    # the { *k: v for k, v in a } syntax? (if it exists?)

    shorthands: dict[str, tuple[IssueField, str]] = {}

    for field in all_fields:
        # All options of this field are unambiguous across all fields' options
        if all(
            all_enum_values.count(into_shorthand(option)) == 1
            for option in field.options
        ):
            shorthands |= {
                into_shorthand(option): (field, option) for option in field.options
            }

    return shorthands


def process_issue_field_input(lhs: str, rhs: str | None) -> tuple[IssueField, str]:
    """
    :param lhs: before the =, or the entire thing if there's no = ((str, None) case)
    :param rhs: after the =, or None if there's no =
    """
    if rhs is None:
        return resolve_issue_field_shorthand(lhs)

    field = find_issue_field(lhs)

    return (field, str(field.normalize_value(rhs)))


def find_issue_field(label: str) -> IssueField:
    for field in available_issue_fields():
        if field.name.lower() == label.lower().strip():
            return field

    raise KeyError(
        f"No issue field named {label!r} exists for this org. "
        f"Available fields: {', '.join(repr(field.name) for field in available_issue_fields())}"
    )


def find_issue_field_by_id(field_id: int) -> IssueField:
    for field in available_issue_fields():
        if field.id == field_id:
            return field

    raise KeyError(
        f"No issue field with id {field_id} exists for this org."
        f"Available fields: {', '.join(f'{field.id} ({field.name})' for field in available_issue_fields())}"
    )


def resolve_issue_field_shorthand(shorthand: str) -> tuple[IssueField, str]:
    for candidate, (field, option) in available_issue_field_shorthands().items():
        if candidate.lower() == shorthand.strip().lower():
            return (field, option)

    raise KeyError(
        f"No shorthand issue field available that corresponds to {shorthand!r}. "
        f"Available shorthands: {', '.join(f':{short} (:{field.name}={value})' for short, (field, value) in available_issue_field_shorthands().items())}. "
        f"An issue field's options are available as shorthands if all of them are unique across every field's options"
    )


@cache
def issue_id(number: int):
    issue_id = call_repo_api("GET", f"issues/{number}", jq=".id")
    if not issue_id:
        raise Exception(f"Could not retrieve issue ID for issue #{number}")
    return int(issue_id)


type HTTPMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]


def call_api(
    method: HTTPMethod,
    route: str,
    jq="",
    bypass_dry_run=False,
    **body_fields: Any,
):
    cmd = ["gh", "api"]
    if method != "GET":
        cmd += ["-X", method]

    if method != "GET" and bypass_dry_run:
        print(
            f"Will [bold]not[/] bypass dry-run for non-GET request [white bold]{method} {route}[/]"
        )
        bypass_dry_run = False

    cmd += [route]

    for key, value in body_fields.items():
        for field in serialize_body_field(key, value):
            cmd += ["-F", field]

    if jq:
        cmd += ["--jq", jq]

    return run(cmd, bypass_dry_run=bypass_dry_run)


def serialize_body_field(key: str, value: Any) -> list[str]:
    # strings, numbers, booleans and nulls are passed as-is (or json-dumped for non-string primitives)
    # array and object values are passed with []= and [key]= syntaxes
    match value:
        case str():
            return [f"{key}={value}"]
        case int() | float() | bool() | None:
            return [f"{key}={json.dumps(value)}"]
        case list():
            # TODO: use [*serialize_body_field(key, item) ...] syntax once we drop support for Python <3.15
            return list(
                chain.from_iterable(
                    [f"{key}[]{ser}" for ser in serialize_body_field("", item)]
                    for item in value
                )
            )
        case dict():
            return list(
                chain.from_iterable(
                    [
                        f"{key}[{subkey}]{ser}"
                        for ser in serialize_body_field("", subvalue)
                    ]
                    for subkey, subvalue in value.items()
                )
            )

        case _:
            raise ValueError(
                f"Unsupported value type for body field {key}: {type(value)}"
            )


def call_repo_api(
    method: HTTPMethod,
    route: str,
    jq="",
    **body_fields: Any,
):
    repo = repo_info()
    return call_api(
        method, f"/repos/{repo.owner}/{repo.repo}/{route}", jq=jq, **body_fields
    )
