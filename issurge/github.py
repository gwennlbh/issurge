import json
from functools import cache
from typing import Any, Literal, NamedTuple

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
        run(["gh", "repo", "view", "--json", "isInOrganization,owner,name"]) or "{}"
    )
    return OwnerInfo(
        in_organization=response["isInOrganization"],
        owner=response["owner"]["login"],
        repo=response["name"],
    )


@cache
def available_issue_types():
    repo = repo_info()
    if not repo.in_organization:
        return []
    response = json.loads(call_api("GET", f"/orgs/{repo.owner}/issue-types") or "[]")
    return [t["name"] for t in response]

type HTTPMethod = Literal["GET", "POST", "PATCH", "DELETE"]

def call_api(
    method: Literal["GET", "POST", "PATCH", "DELETE"], route: str, **body_fields: Any
):
    cmd = ["gh", "api"]
    if method != "GET":
        cmd += ["-X", method]

    cmd += [route]

    for key, value in body_fields.items():
        if type(value) is str:
            cmd += ["-F", f"{key}={value}"]
        else:
            cmd += ["-F", f"{key}={json.dumps(value)}"]

    return run(cmd)

def call_repo_api(
    method: Literal["GET", "POST", "PATCH", "DELETE"], route: str, **body_fields: Any
):
    repo = repo_info()
    return call_api(method, f"/repos/{repo.owner}/{repo.repo}/{route}", **body_fields)
