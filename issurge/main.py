#!/usr/bin/env python
"""
Usage:
    issurge  [options] <file> [--] [<glab-args>...]
    issurge --help

<glab-args> contains arguments that will be passed as-is to the end of all `glab' commands

Options:
    --dry-run   Don't actually post the issues
    --debug     Print debug information
"""
import json
from collections.abc import Iterable
from subprocess import run
import subprocess
from rich import print
from pathlib import Path
from typing import Any, Generator, NamedTuple, TypeAlias, TypeVar
from docopt import docopt

def run():
    opts = docopt(__doc__)
    TAB = "\t"

    def debug(*args, **kwargs):
        if opts["--debug"]:
            print(*args, **kwargs)

    debug(f"Running with options: {opts}")

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

        def as_dict(self):
            if len(self.children) > 1:
                child_dicts = {}
                for node in self.children:
                    child_dicts |= node.as_dict()
                return {self.text: child_dicts}
            elif len(self.children) == 1:
                return {self.text: self.children[0].as_dict()}
            else:
                return {self.text: None}


    def indented_to_dict(to_parse: str) -> dict[str, Any]:
        root = Node("root")
        root.add_children([Node(line) for line in to_parse.splitlines() if line.strip()])
        return root.as_dict()["root"]


    class Issue(NamedTuple):
        title: str
        description: str
        labels: set[str]
        assignees: set[str]
        milestone: str

        def __str__(self) -> str:
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

        def submit(self):
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
            command.extend(opts["<glab-args>"])
            if opts['--dry-run'] or opts['--debug']:
                print(
                    f"{'Would run' if opts['--dry-run'] else 'Running'} [white bold]{subprocess.list2cmdline(command)}[/]"
                )
            if not opts["--dry-run"]:
                subprocess.run(command)

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
            for word in raw.split(" "):
                if word.startswith("~"):
                    labels.add(word[1:])
                elif word.startswith("%"):
                    milestone = word[1:]
                elif word.startswith("@"):
                    assignees.add(word[1:])
                else:
                    title += f" {word}"

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


    issues: list[Issue] = []


    def dict_to_issue(
        issue_fragment: str,
        children: dict[str, Any],
        current_issue: Issue,
        recursion_depth=0,
    ) -> list[Issue]:
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
            log(f"Made {current_issue!s}")
            return [current_issue]

        if not expecting_description and children is not None:
            result = []
            log(f"Making children from {current_issue!s}")
            for child, grandchildren in children.items():
                result.extend(
                    dict_to_issue(child, grandchildren, current_issue, recursion_depth + 1)
                )
            return result

        log(f"[red bold]Issue {issue_fragment!r} has no title and no children[/red bold]")
        return []


    for item in indented_to_dict(Path(opts["<file>"]).read_text()).items():
        issue = dict_to_issue(*item, Issue("", "", set(), set(), ""))
        issues.extend(issue)

    print("Submitting issues...")
    for issue in issues:
        # debug(issue)
        issue.submit()
