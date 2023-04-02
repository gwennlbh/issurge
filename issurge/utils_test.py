import os, io, sys
from unittest.mock import Mock
from ward import test
from issurge.utils import debug, debugging, dry_running
import issurge.utils


@test("debugging is false by default")
def _():
    assert not debugging()


@test("debugging is true when ISSURGE_DEBUG is set")
def _():
    os.environ["ISSURGE_DEBUG"] = "1"
    assert debugging()
    del os.environ["ISSURGE_DEBUG"]


@test("dry_running is false by default")
def _():
    assert not dry_running()


@test("dry_running is true when ISSURGE_DRY_RUN is set")
def _():
    os.environ["ISSURGE_DRY_RUN"] = "1"
    assert dry_running()
    del os.environ["ISSURGE_DRY_RUN"]


@test("debug only prints when debugging is true")
def _():
    issurge.utils.print = Mock()
    os.environ["ISSURGE_DEBUG"] = "1"
    debug("debug")
    assert len(issurge.utils.print.mock_calls) == 1
    assert issurge.utils.print.mock_calls[0].args[0] == "debug"
