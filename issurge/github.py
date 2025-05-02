import json
from functools import cache
from typing import NamedTuple

from issurge.utils import run


class OwnerInfo(NamedTuple):
    in_organization: bool
    owner: str
    repo: str

    def __rich_repr__(self):
        yield "isInOrganization", self.isInOrganization, False
        yield "owner", self.owner, ""
        yield "repo", self.repo, ""


@cache
def repo_info():
    print("not stubbed :(")
    response = json.loads(
        run(["gh", "repo", "view", "--json", "isInOrganization,owner,name"])
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
    response = json.loads(run(["gh", "api", f"/orgs/{repo.owner}/issue-types"]))
    return [t["name"] for t in response]
