import re
import subprocess
from sys import exit
from typing import Any, Iterable, Literal, NamedTuple
from urllib.parse import urlparse

from rich import print

from issurge import github
from issurge.utils import NEWLINE, TAB, debug, run


class Node:
    def __init__(self, indented_line):
        self.children = []
        self.level = len(indented_line) - len(indented_line.lstrip())
        self.text = indented_line.strip()

    def add_children(self, nodes):
        childlevel = nodes[0].level
        while nodes:
            node = nodes.pop(0)
            if node.level == childlevel:  # add node as a child
                self.children.append(node)
            elif (
                node.level > childlevel
            ):  # add nodes as grandchildren of the last child
                nodes.insert(0, node)
                self.children[-1].add_children(nodes)
            elif node.level <= self.level:  # this node is a sibling, no more children
                nodes.insert(0, node)
                return

    def as_dict(self) -> dict[str, Any]:
        if len(self.children) > 1:
            child_dicts = {}
            for node in self.children:
                child_dicts |= node.as_dict()
            return {self.text: child_dicts}
        elif len(self.children) == 1:
            return {self.text: self.children[0].as_dict()}
        else:
            return {self.text: None}

    @staticmethod
    def to_dict(to_parse: str) -> dict[str, Any]:
        if not to_parse.strip():
            return {}
        root = Node("root")
        root.add_children(
            [Node(line) for line in to_parse.splitlines() if line.strip()]
        )
        return root.as_dict()["root"]


# type IssueReference = tuple[Literal["reference", "direct"], int]
class IssueReference(NamedTuple):
    type: Literal["reference", "direct"]
    number: int

    def __str__(self) -> str:
        match self.type:
            case "reference":
                return f".{self.number}"
            case "direct":
                return f"{self.number}"

    def resolved(
        self, resolutions: dict[int, int], strict: bool
    ) -> "IssueReference | None":
        if self.type != "reference":
            return self

        if resolved := resolutions.get(self.number):
            return IssueReference("direct", resolved)

        if strict:
            raise Exception(f"Could not resolve reference #{self.number}")
        return None


class Issue(NamedTuple):
    title: str = ""
    description: str = ""
    labels: set[str] = set()
    assignees: set[str] = set()
    milestone: str = ""
    reference: int | None = None
    # Direct means that the number refers to an actual github issue, where as reference means that it refers to a .N issue reference, in the same way that #.N references work in descriptions.
    parent: IssueReference | None = None
    blocked_by: set[IssueReference] = set()

    def __rich_repr__(self):
        yield self.title
        yield "description", self.description, ""
        yield "labels", self.labels, set()
        yield "assignees", self.assignees, set()
        yield "milestone", self.milestone, ""
        yield "ref", self.reference, None
        yield "references", self.references, set()
        yield "parent", self.parent, None
        yield "blocked_by", self.blocked_by, set()

    def __str__(self) -> str:
        result = ""
        if self.reference:
            result += f"<#{self.reference}> "
        result += f"{self.title}" or "<No title>"
        if self.parent:
            result += f" ^{self.parent}"
        if self.labels:
            result += f" {' '.join(['~' + l for l in self.labels])}"
        if self.blocked_by:
            result += f" {' '.join(['>' + str(ref) for ref in self.blocked_by])}"
        if self.milestone:
            result += f" %{self.milestone}"
        if self.assignees:
            result += f" {' '.join(['@' + a for a in self.assignees])}"
        if self.description:
            result += f": {self.description}"
        return result

    def __or__(self, new_data: "Issue") -> "Issue":
        return Issue(
            title=new_data.title or self.title,
            description=new_data.description or self.description,
            labels=self.labels | new_data.labels,
            assignees=self.assignees | new_data.assignees,
            milestone=new_data.milestone or self.milestone,
            reference=new_data.reference or self.reference,
            parent=new_data.parent or self.parent,
            blocked_by=new_data.blocked_by | self.blocked_by,
        )

    def display(self) -> str:
        result = ""
        if self.reference:
            result += f"[bold blue]<#{self.reference}>[/bold blue] "
        if self.parent:
            result += f"[blue dim]^{self.parent}[/blue dim] "
        result += f"[white]{self.title[:30]}[/white]" or "[red]<No title>[/red]"
        if len(self.title) > 30:
            result += " [white dim](...)[/white dim]"
        if self.blocked_by:
            result += f" [yellow]{' '.join(['>' + str(ref) for ref in self.blocked_by])}[/yellow]"
        if self.labels:
            result += (
                f" [yellow]{' '.join(['~' + l for l in self.labels][:4])}[/yellow]"
            )
            if len(self.labels) > 4:
                result += " [yellow dim]~...[/yellow dim]"
        if self.milestone:
            result += f" [purple]%{self.milestone}[/purple]"
        if self.assignees:
            result += f" [cyan]{' '.join(['@' + a for a in self.assignees])}[/cyan]"
        if self.description:
            result += " [white][...][/white]"
        return result

    @property
    def references(self) -> set[int]:
        # find all #\.(\d+)\b in description
        references = set()
        for match in re.finditer(
            r"#\.(?P<num>\d+)(\b|$)", self.description, flags=re.MULTILINE
        ):
            references.add(int(match.group("num")))

        return references

    def resolve_references(
        self, resolution_map: dict[int, int], strict=False
    ) -> "Issue":
        resolved_description = self.description
        for reference in self.references:
            if resolved := resolution_map.get(reference):
                resolved_description = resolved_description.replace(
                    f"#.{reference}", f"#{resolved}"
                )
            elif strict:
                raise Exception(f"Could not resolve reference #.{reference}")

        parent = self.parent.resolved(resolution_map, strict) if self.parent else None

        blocked_by = {ref.resolved(resolution_map, strict) for ref in self.blocked_by}
        blocked_by = {ref for ref in blocked_by if ref is not None}

        return Issue(
            **(
                self._asdict()
                | {
                    "description": resolved_description,
                    "parent": parent,
                    "blocked_by": blocked_by,
                }
            )
        )

    def submit(self, submitter_args: list[str]) -> tuple[str | None, int | None]:
        remote_url = self._get_remote_url()
        if remote_url.hostname == "github.com":
            return self._github_submit(submitter_args)
        else:
            return self._gitlab_submit(submitter_args)

    def _get_remote_url(self):
        try:
            origin = subprocess.run(
                ["git", "remote", "get-url", "origin"], capture_output=True
            ).stdout.decode()
            # fake an HTTPs URL from a SSH one
            if origin.startswith("git@"):
                origin = origin.replace(":", "/").replace("git@", "https://")
            return urlparse(origin)
        except subprocess.CalledProcessError as e:
            raise ValueError(
                "Could not determine remote url, make sure that you are inside of a git repository that has a remote named 'origin'"
            ) from e

    def _gitlab_submit(
        self, submitter_args: list[str]
    ) -> tuple[str | None, int | None]:
        command = ["glab", "issue", "new"]
        if self.title:
            command += ["-t", self.title]
        command += ["-d", self.description or ""]
        for a in self.assignees:
            command += ["-a", a if a != "me" else "@me"]
        for l in self.labels:
            command += ["-l", l]
        if self.milestone:
            command += ["-m", self.milestone]
        command.extend(submitter_args)
        out = run(command)
        # parse issue number from command output url: https://.+/-/issues/(\d+)
        if out and (url := re.search(r"https://.+/-/issues/(\d+)", out)):
            return url.group(0), int(url.group(1))

        # raise Exception(f"Could not parse issue number from {out!r}")
        return None, None

    def _github_submit(
        self, submitter_args: list[str]
    ) -> tuple[str | None, int | None]:
        available_issue_types = github.available_issue_types()
        issue_types_to_add = [
            t
            for t in available_issue_types
            if t.lower() in (l.lower() for l in self.labels)
        ]

        if len(issue_types_to_add) > 1:
            print(
                f"[red bold]Cannot add multiple issue types: [/] {', '.join(issue_types_to_add)}"
            )
            exit(1)

        issue_type = issue_types_to_add[0] if issue_types_to_add else None

        command = ["gh", "issue", "new"]
        if self.title:
            command += ["-t", self.title]
        command += ["-b", self.description or ""]
        for a in self.assignees:
            command += ["-a", a if a != "me" else "@me"]
        for l in self.labels:
            # issue type will be set later with a REST API call
            # (see https://github.com/cli/cli/issues/9696)
            if issue_type and l.lower() == issue_type.lower():
                continue
            command += ["-l", l]
        if self.milestone:
            command += ["-m", self.milestone]
        command.extend(submitter_args)
        out = run(command)
        # parse issue number from command output url: https://github.com/.+/issues/(\d+)
        pattern = re.compile(r"https:\/\/github\.com\/.+\/issues\/(\d+)")

        if out and (url := pattern.search(out)):
            number = int(url.group(1))

            if issue_type:
                github.call_repo_api(
                    "PATCH",
                    f"issues/{number}",
                    type=issue_type,
                )

            match self.parent:
                case None:
                    pass
                case IssueReference("reference", _):
                    raise Exception(
                        "Cannot set a reference-style parent on GitHub, only direct-style"
                    )

                case IssueReference("direct", parent_number):
                    github.call_repo_api(
                        "POST",
                        f"issues/{parent_number}/sub_issues",
                        sub_issue_id=github.issue_id(number),
                        replace_parent=True,
                    )

            if self.blocked_by:
                if any(ref.type == "reference" for ref in self.blocked_by):
                    raise Exception(
                        "Cannot set reference-style blocked_on on GitHub, only direct-style"
                    )

                for ref in self.blocked_by:
                    github.call_repo_api(
                        "POST",
                        f"issues/{number}/dependencies/blocked_by",
                        issue_id=github.issue_id(ref.number),
                    )

            return url.group(0), number

        # raise Exception(f"Could not parse issue number from {out!r}, looked for regex {pattern}")
        return None, None

    @staticmethod
    def _word_and_sigil(raw_word: str) -> tuple[str, str]:
        if raw_word.startswith("#.") and raw_word[2:].isdigit():
            return "#.", raw_word[2:]
        if raw_word.startswith("^.") and raw_word[2:].isdigit():
            return "^.", raw_word[2:]
        if raw_word.startswith("^") and raw_word[1:].isdigit():
            return "^", raw_word[1:]
        if raw_word.startswith(">.") and raw_word[2:].isdigit():
            return ">.", raw_word[2:]
        if raw_word.startswith(">") and raw_word[1:].isdigit():
            return ">", raw_word[1:]

        sigil = raw_word[0]
        word = raw_word[1:]
        if sigil not in ("~", "%", "@"):
            sigil = ""
            word = raw_word
        return sigil, word

    # The boolean is true if the issue expects a description (ending ':')
    @classmethod
    def parse(cls, raw: str) -> tuple["Issue", bool]:
        raw = raw.strip()
        expects_description = False
        if raw.endswith(":"):
            expects_description = True
            raw = raw[:-1].strip()

        title = ""
        parent: IssueReference | None = None
        description = ""
        labels: set[str] = set()
        assignees: set[str] = set()
        blocked_by: set[IssueReference] = set()
        milestone = ""
        reference: int | None = None
        # only labels/milestones/assignees at the beginning or end of the line are not added to the title as words
        add_to_title = False
        remaining_words = [word.strip() for word in raw.split(" ") if word.strip()]
        _debug_sigils = []

        while remaining_words:
            sigil, word = cls._word_and_sigil(remaining_words.pop(0))

            _debug_sigils.append(sigil)

            if sigil and add_to_title:
                title += f" {word}"

            match sigil:
                case "~":
                    labels.add(word)
                case "%":
                    milestone = word
                case "@":
                    assignees.add(word)
                case "^":
                    parent = IssueReference("direct", int(word))
                case "^.":
                    parent = IssueReference("reference", int(word))
                case ">":
                    blocked_by.add(IssueReference("direct", int(word)))
                case ">.":
                    blocked_by.add(IssueReference("reference", int(word)))
                case "#.":
                    reference = int(word)
                case _:
                    title += f" {word}"
                    # add to title if there are remaining regular words
                    add_to_title = any(
                        not sigil
                        for (sigil, _) in map(cls._word_and_sigil, remaining_words)
                    )

        return (
            cls(
                title=title.strip(),
                description=description,
                labels=labels,
                assignees=assignees,
                milestone=milestone,
                reference=reference,
                parent=parent,
                blocked_by=blocked_by,
            ),
            expects_description,
        )


def tree_to_text(tree: dict[str, Any], recursion_depth=0) -> str:
    result = ""
    for line, children in tree.items():
        result += TAB * recursion_depth + line.strip() + NEWLINE
        if children is not None:
            result += tree_to_text(children, recursion_depth + 1)
    return result


def process_description(description: str) -> Issue:
    """
    Returns a Issue with the following fields set:
    - description: the original description, but with >N and >.N, ^N and ^.N replaced by #.N or #N
    - blocked_by: a set of IssueReferences for each >N and >.N in the description
    - parent: an IssueReference for the first ^N or ^.N in the description
    """
    blocked_by: set[IssueReference] = set()
    parent: IssueReference | None = None

    # Find >N or >.N in the description
    for match in re.finditer(r"([>^]\.?)(\d+)", description):
        sigil, num = match.groups()

        match sigil:
            case ">":
                blocked_by.add(IssueReference("direct", int(num)))
            case ">.":
                blocked_by.add(IssueReference("reference", int(num)))
            # Not sure about these
            case "^":
                parent = IssueReference("direct", int(num))
            case "^.":
                parent = IssueReference("reference", int(num))

        # Replace match with #.N or #N in the description
        description = (
            description[: match.start()]
            + "#"
            + sigil[1:]
            + num
            + description[match.end() :]
        )

    return Issue(
        description=description,
        blocked_by=blocked_by,
        parent=parent,
    )


def parse_issue_fragment(
    issue_fragment: str,
    children: dict[str, Any],
    current_issue: Issue,
    recursion_depth=0,
    cli_options: dict[str, Any] | None = None,
) -> list[Issue]:
    if not cli_options:
        cli_options = {}
    log = lambda *args, **kwargs: print(
        f"[white]{issue_fragment[:50]: <50}[/white]\t{TAB * recursion_depth}",
        *args,
        **kwargs,
    )

    if issue_fragment.strip().startswith("//"):
        log(f"[yellow bold]Skipping comment[/]")
        return []
    log(f"Inheriting from {current_issue.display()}")

    parsed, expecting_description = Issue.parse(issue_fragment)

    current_issue |= parsed

    if expecting_description:
        log(f"[white dim]{parsed} expects a description[/]")
        if children is None:
            raise ValueError(f"Expected a description after {issue_fragment!r}")

        current_issue |= process_description(tree_to_text(children, 0))

    if current_issue.title:
        log(f"Made {current_issue.display()}")
        return [current_issue]

    if not expecting_description and children is not None:
        result = []
        log(f"Making children from {current_issue.display()}")
        for child, grandchildren in children.items():
            result.extend(
                parse_issue_fragment(
                    child,
                    grandchildren,
                    current_issue,
                    recursion_depth + 1,
                    cli_options,
                )
            )
        return result

    log(f"[red bold]Issue {issue_fragment!r} has no title and no children[/red bold]")
    return []


def parse(raw: str) -> Iterable[Issue]:
    for item in Node.to_dict(raw).items():
        debug(f"Processing {item!r}")
        for issue in parse_issue_fragment(*item, Issue("", "", set(), set(), "")):
            yield issue
