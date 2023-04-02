import os
import subprocess
from typing import Any, Iterable, NamedTuple
from urllib.parse import urlparse

from rich import print

from issurge.utils import NEWLINE, TAB, debug, debugging, dry_running


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
        root = Node("root")
        root.add_children(
            [Node(line) for line in to_parse.splitlines() if line.strip()]
        )
        return root.as_dict()["root"]


class Issue(NamedTuple):
    title: str = ""
    description: str = ""
    labels: set[str] = set()
    assignees: set[str] = set()
    milestone: str = ""

    def __rich_repr__(self):
        yield self.title
        yield "description", self.description, ""
        yield "labels", self.labels, set()
        yield "assignees", self.assignees, set()
        yield "milestone", self.milestone, ""

    def __str__(self) -> str:
        result = f"{self.title}" or "<No title>"
        if self.labels:
            result += f" {' '.join(['~' + l for l in self.labels])}"
        if self.milestone:
            result += f" %{self.milestone}"
        if self.assignees:
            result += f" {' '.join(['@' + a for a in self.assignees])}"
        if self.description:
            result += f": {self.description}"
        return result

    def display(self) -> str:
        result = f"[white]{self.title[:30]}[/white]" or "[red]<No title>[/red]"
        if len(self.title) > 30:
            result += " [white dim](...)[/white dim]"
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

    def submit(self, submitter_args: list[str]):
        remote_url = self._get_remote_url()
        if remote_url.hostname == "github.com":
            self._github_submit(submitter_args)
        else:
            self._gitlab_submit(submitter_args)

    def _get_remote_url(self):
        try:
            return urlparse(
                subprocess.run(
                    ["git", "remote", "get-url", "origin"], capture_output=True
                ).stdout.decode()
            )
        except subprocess.CalledProcessError as e:
            raise ValueError(
                "Could not determine remote url, make sure that you are inside of a git repository that has a remote named 'origin'"
            ) from e

    def _gitlab_submit(self, submitter_args: list[str]):
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
        self._run(command)

    def _github_submit(self, submitter_args: list[str]):
        command = ["gh", "issue", "new"]
        if self.title:
            command += ["-t", self.title]
        command += ["-b", self.description or ""]
        for a in self.assignees:
            command += ["-a", a if a != "me" else "@me"]
        for l in self.labels:
            command += ["-l", l]
        if self.milestone:
            command += ["-m", self.milestone]
        command.extend(submitter_args)
        self._run(command)

    def _run(self, command):
        if dry_running() or debugging():
            print(
                f"{'Would run' if dry_running() else 'Running'} [white bold]{subprocess.list2cmdline(command)}[/]"
            )
        if not dry_running():
            try:
                subprocess.run(command, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(
                    f"Calling [white bold]{e.cmd}[/] failed with code [white bold]{e.returncode}[/]:\n{NEWLINE.join(TAB + line for line in e.stderr.decode().splitlines())}"
                )

    @staticmethod
    def _word_and_sigil(raw_word: str) -> tuple[str, str]:
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
        description = ""
        labels = set()
        assignees = set()
        milestone = ""
        # only labels/milestones/assignees at the beginning or end of the line are not added to the title as words
        add_to_title = False
        remaining_words = [word.strip() for word in raw.split(" ") if word.strip()]

        while remaining_words:
            sigil, word = cls._word_and_sigil(remaining_words.pop(0))

            if sigil and add_to_title:
                title += f" {word}"

            match sigil:
                case "~":
                    labels.add(word)
                case "%":
                    milestone = word
                case "@":
                    assignees.add(word)
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
            ),
            expects_description,
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
    log = lambda *args, **kwargs: debug(
        f"[white]{issue_fragment[:50]: <50}[/white]\t{TAB*recursion_depth}",
        *args,
        **kwargs,
    )

    if issue_fragment.strip().startswith("//"):
        log(f"[yellow bold]Skipping comment[/]")
        return []
    current_title = current_issue.title
    current_description = current_issue.description
    current_labels = set(current_issue.labels)
    current_assignees = set(current_issue.assignees)
    current_milestone = current_issue.milestone

    parsed, expecting_description = Issue.parse(issue_fragment)
    if expecting_description:
        log(f"[white dim]{parsed} expects a description[/]")

    current_title = parsed.title
    current_labels |= parsed.labels
    current_assignees |= parsed.assignees
    current_milestone = parsed.milestone
    if expecting_description:
        if children is None:
            raise ValueError(f"Expected a description after {issue_fragment!r}")
        current_description = ""
        for line, v in children.items():
            if v is not None:
                raise ValueError(
                    "Description should not have indented lines at {line!r}"
                )
            current_description += f"{line.strip()}\n"

    current_issue = Issue(
        title=current_title,
        description=current_description,
        labels=current_labels,
        assignees=current_assignees,
        milestone=current_milestone,
    )

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
        for issue in parse_issue_fragment(*item, Issue("", "", set(), set(), "")):
            yield issue
