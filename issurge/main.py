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
import os
from collections.abc import Iterable
from pathlib import Path
from subprocess import run
from typing import Generator, TypeAlias, TypeVar

from docopt import docopt
from rich import print

from issurge.parser import parse
from issurge.utils import debug


def run():
    opts = docopt(__doc__)
    os.environ["ISSURGE_DEBUG"] = "1" if opts["--debug"] else ""

    debug(f"Running with options: {opts}")
    print("Submitting issues...")
    for issue in parse(Path(opts["<file>"]).read_text()):
        issue.submit()
