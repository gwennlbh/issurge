import json
from itertools import chain
from functools import cache
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


@cache
def available_issue_fields() -> dict[str, int]:
    repo = repo_info()

    if not repo.in_organization:
        return {}

    return json.loads(
        call_api(
            "GET",
            f"/orgs/{repo.owner}/issue-fields",
            jq="map({(.name): .id}) | add",
            bypass_dry_run=True,
        )
        or "{}"
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
