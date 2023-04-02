#!/usr/bin/env python
"""
Usage:
    issurge  [options] <file> [--] [<submitter-args>...]
    issurge --help

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


def run(opts=None):
    opts = opts or docopt(__doc__)
    os.environ["ISSURGE_DEBUG"] = "1" if opts["--debug"] else ""
    os.environ["ISSURGE_DRY_RUN"] = "1" if opts["--dry-run"] else ""

    debug(f"Running with options: {opts}")
    print("Submitting issues...")
    for issue in parse(Path(opts["<file>"]).read_text()):
        issue.submit(opts["<submitter-args>"])
