#!/usr/bin/env python
"""
Usage:
    issurge [options] new <words>...
    issurge [options] <file> [--] [<submitter-args>...]
    issurge --help
    issurge --help-syntax

issurge new <words>... acts like echo <words>... | issurge /dev/stdin, but also asks for a description if the issue ends with `:'.

<submitter-args> contains arguments that will be passed as-is to the end of all `glab' commands

Options:
    --dry-run   Don't actually post the issues
    --debug     Print debug information
    --open      Open every created issue in the browser

Syntax:

{quick_syntax_help}

Use --help-syntax for the full help.

issurge v{version}
"""

import importlib.resources
import os
import webbrowser
from importlib.metadata import version
from pathlib import Path

from docopt import docopt
from rich import print
from rich.markdown import Markdown
from rich.text import Text

from issurge import interactive
from issurge.parser import parse
from issurge.utils import debug, dry_running, lines_between, render_to_ansi

assets = importlib.resources.files(__package__)
syntax_help = (assets / "SYNTAX.md").read_text(encoding="utf-8")
quick_syntax_help = "\n".join(
    lines_between("<!-- cli-help -->", "<!-- /cli-help -->", syntax_help)
)


def run(opts=None):
    opts = opts or docopt(
        (__doc__ or "").format(
            version=Text(version("issurge")).stylize("blue"),
            quick_syntax_help=render_to_ansi(Markdown(quick_syntax_help)),
        )
    )

    os.environ["ISSURGE_DEBUG"] = "1" if opts["--debug"] else ""
    os.environ["ISSURGE_DRY_RUN"] = "1" if opts["--dry-run"] else ""

    debug(f"Running with options: {opts}")
    if opts["--help-syntax"]:
        print(Markdown(syntax_help))
    elif opts["new"]:
        issue = interactive.create_issue(" ".join(opts["<words>"]))
        debug(f"Submitting {issue.display()}")
        number, url = issue.submit(opts["<submitter-args>"])
        print(f"Created issue #{number}: {url}")
    else:
        print("Submitting issues...")
        references_resolutions: dict[int, int] = {}
        for issue in parse(Path(opts["<file>"]).read_text(encoding="utf-8")):
            issue = issue.resolve_references(
                references_resolutions, strict=not dry_running()
            )
            url, number = issue.submit(opts["<submitter-args>"])
            print(f"Created issue #{number}: {url}")
            if issue.reference and number:
                references_resolutions[issue.reference] = number
            if opts["--open"] and url:
                webbrowser.open(url)
