import os
import re
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
        if not to_parse.strip():
            return {}
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
    reference: int|None = None

    def __rich_repr__(self):
        yield self.title
        yield "description", self.description, ""
        yield "labels", self.labels, set()
        yield "assignees", self.assignees, set()
        yield "milestone", self.milestone, ""
        yield "ref", self.reference, None
        yield "references", self.references, set()

    def __str__(self) -> str:
        result = ""
        if self.reference:
            result += f"<#{self.reference}> "
        result += f"{self.title}" or "<No title>"
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
        result = ""
        if self.reference:
            result += f"[bold blue]<#{self.reference}>[/bold blue] "
        result += f"[white]{self.title[:30]}[/white]" or "[red]<No title>[/red]"
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

    @property
    def references(self) -> set[int]:
        # find all \b#\.(\d+)\b in description
        references = set()
        for word in self.description.strip().split(" "):
            if word.startswith("#.") and word[2:].strip().isdigit():
                references.add(int(word[2:].strip()))

        return references

    def resolve_references(self, resolution_map: dict[int, int], strict=False) -> 'Issue':
        resolved_description = self.description
        for reference in self.references:
            if (resolved := resolution_map.get(reference)):
                resolved_description = resolved_description.replace(f"#.{reference}", f"#{resolved}")
            elif strict:
                raise Exception(f"Could not resolve reference #.{reference}")

        return Issue(**(self._asdict() | {"description": resolved_description}))
            

    def submit(self, submitter_args: list[str]):
        remote_url = self._get_remote_url()
        if remote_url.hostname == "github.com":
            return self._github_submit(submitter_args)
        else:
            return self._gitlab_submit(submitter_args)

    def _get_remote_url(self):
        try:
            origin =  subprocess.run(
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

    def _gitlab_submit(self, submitter_args: list[str]) -> int|None:
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
        out = self._run(command)
        # parse issue number from command output url: https://.+/-/issues/(\d+)
        if out and (url := re.search(r"https://.+/-/issues/(\d+)", out)):
            return int(url.group(1))
        
        # raise Exception(f"Could not parse issue number from {out!r}")

    def _github_submit(self, submitter_args: list[str]) -> int|None:
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
        out = self._run(command)
        # parse issue number from command output url: https://github.com/.+/issues/(\d+)
        pattern = re.compile(r"https:\/\/github\.com\/.+\/issues\/(\d+)")
        if out and (url := pattern.search(out)):
            return int(url.group(1))

        # raise Exception(f"Could not parse issue number from {out!r}, looked for regex {pattern}")
        return None

    def _run(self, command):
        if dry_running() or debugging():
            print(
                f"{'Would run' if dry_running() else 'Running'} [white bold]{subprocess.list2cmdline(command)}[/]"
            )
        if not dry_running():
            try:
                out = subprocess.run(command, check=True, capture_output=True)
                return out.stderr.decode() + "\n" + out.stdout.decode()
            except subprocess.CalledProcessError as e:
                print(
                    f"Calling [white bold]{e.cmd}[/] failed with code [white bold]{e.returncode}[/]:\n{NEWLINE.join(TAB + line for line in e.stderr.decode().splitlines())}"
                )

    @staticmethod
    def _word_and_sigil(raw_word: str) -> tuple[str, str]:
        if raw_word.startswith("#.") and raw_word[2:].isdigit():
            return "#.", raw_word[2:]

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
        reference = None
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
                reference=reference 
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
        f"[white]{issue_fragment[:50]: <50}[/white]\t{TAB*recursion_depth}",
        *args,
        **kwargs,
    )

    if issue_fragment.strip().startswith("//"):
        log(f"[yellow bold]Skipping comment[/]")
        return []
    log(f"Inheriting from {current_issue.display()}")
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
    if parsed.milestone:
        current_milestone = parsed.milestone
    if expecting_description:
        if children is None:
            raise ValueError(f"Expected a description after {issue_fragment!r}")
        current_description = tree_to_text(children, 0)

    current_issue = Issue(
        title=current_title,
        description=current_description,
        labels=current_labels,
        assignees=current_assignees,
        milestone=current_milestone,
        reference=parsed.reference
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
        debug(f"Processing {item!r}")
        for issue in parse_issue_fragment(*item, Issue("", "", set(), set(), "")):
            yield issue
