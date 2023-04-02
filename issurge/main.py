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
"""
import os
from pathlib import Path

from docopt import docopt
from rich import print

from issurge.parser import parse
from issurge.utils import debug
from issurge import interactive


def run(opts=None):
    opts = opts or docopt(__doc__)
    os.environ["ISSURGE_DEBUG"] = "1" if opts["--debug"] else ""
    os.environ["ISSURGE_DRY_RUN"] = "1" if opts["--dry-run"] else ""

    debug(f"Running with options: {opts}")
    if opts["new"]:
        issue = interactive.create_issue(" ".join(opts["<words>"]))
        debug(f"Submitting {issue.display()}")
        issue.submit(opts["<submitter-args>"])
    else:
        print("Submitting issues...")
        for issue in parse(Path(opts["<file>"]).read_text()):
            issue.submit(opts["<submitter-args>"])
