#!/usr/bin/env python
"""
Usage:
    issurge [options] new <words>...
    issurge [options] <file> [--] [<submitter-args>...]
    issurge --help

issurge new <words>... acts like echo <words>... | issurge /dev/stdin, but also asks for a description if the issue ends with `:'.

<submitter-args> contains arguments that will be passed as-is to the end of all `glab' commands

Options:
    --dry-run   Don't actually post the issues
    --debug     Print debug information
    --open      Open every created issue in the browser
"""

import os
from pathlib import Path
import webbrowser

from docopt import docopt
from rich import print

from issurge.parser import parse
from issurge.utils import debug, dry_running
from issurge import interactive


def run(opts=None):
    opts = opts or docopt(__doc__)
    os.environ["ISSURGE_DEBUG"] = "1" if opts["--debug"] else ""
    os.environ["ISSURGE_DRY_RUN"] = "1" if opts["--dry-run"] else ""

    debug(f"Running with options: {opts}")
    if opts["new"]:
        issue = interactive.create_issue(" ".join(opts["<words>"]))
        debug(f"Submitting {issue.display()}")
        number = issue.submit(opts["<submitter-args>"])
        print(f"Created issue #{number}")
    else:
        print("Submitting issues...")
        references_resolutions: dict[int, int] = {}
        for issue in parse(Path(opts["<file>"]).read_text()):
            issue = issue.resolve_references(
                references_resolutions, strict=not dry_running()
            )
            url, number = issue.submit(opts["<submitter-args>"])
            print(f"Created issue #{number}")
            if issue.reference and number:
                references_resolutions[issue.reference] = number
            if opts["--open"] and url:
                webbrowser.open(url)
