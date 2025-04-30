import os
from unittest.mock import Mock

import pytest

import issurge.utils
from issurge.utils import debug, debugging, dry_running


def test_debugging_is_false_by_default():
    assert not debugging()


def test_debugging_is_true_when_issurge_debug_is_set():
    os.environ["ISSURGE_DEBUG"] = "1"
    assert debugging()
    del os.environ["ISSURGE_DEBUG"]


def test_dry_running_is_false_by_default():
    assert not dry_running()


def test_dry_running_is_true_when_issurge_dry_run_is_set():
    os.environ["ISSURGE_DRY_RUN"] = "1"
    assert dry_running()
    del os.environ["ISSURGE_DRY_RUN"]


def test_debug_only_prints_when_debugging_is_true():
    issurge.utils.print = Mock()
    os.environ["ISSURGE_DEBUG"] = "1"
    debug("debug")
    assert len(issurge.utils.print.mock_calls) == 1
    assert issurge.utils.print.mock_calls[0].args[0] == "debug"
    del os.environ["ISSURGE_DEBUG"]
