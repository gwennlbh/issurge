import os
from urllib.parse import urlparse
from ward import fixture, test
from issurge.main import run
from pathlib import Path
from unittest.mock import Mock
from issurge.parser import Issue, subprocess

from issurge.utils import debugging, dry_running


@fixture
def setup():
    Path("test_empty_issues").write_text("")
    Path("test_some_issues").write_text(
        """~common @common %common
\tAn issue to submit
Another ~issue to submit @me"""
    )
    subprocess.run = Mock()
    Issue._get_remote_url = Mock(
        return_value=urlparse("https://github.com/ewen-lbh/gh-api-playground")
    )
    yield
    Path("test_empty_issues").unlink()
    Path("test_some_issues").unlink()
    del os.environ["ISSURGE_DEBUG"]
    del os.environ["ISSURGE_DRY_RUN"]


@fixture
def default_opts():
    yield {
        "<submitter-args>": [],
        "<file>": "test_empty_issues",
        "<words>": [],
        "new": False,
        "--dry-run": False,
        "--debug": False,
    }


@test("dry run is set when --dry-run is passed")
def _(_=setup, opts=default_opts):
    run(opts=opts | {"--dry-run": True})
    assert dry_running()
    assert not debugging()


@test("debug is set when --debug is passed")
def _(_=setup, opts=default_opts):
    run(opts=opts | {"--debug": True})
    assert debugging()
    assert not dry_running()


@test("dry run and debug are not set by default")
def _(_=setup, opts=default_opts):
    run(opts=opts)
    assert not dry_running()
    assert not debugging()


@test("both dry run and debug are set when both are passed")
def _(_=setup, opts=default_opts):
    run(opts=opts | {"--dry-run": True, "--debug": True})
    assert dry_running()
    assert debugging()


@test("issues are submitted when --dry-run is not passed, with github provider")
def _(_=setup, opts=default_opts):
    run(opts=opts | {"<file>": "test_some_issues"})
    assert [call.args[0] for call in subprocess.run.mock_calls] == [
        [
            "gh",
            "issue",
            "new",
            "-t",
            "An issue to submit",
            "-b",
            "",
            "-a",
            "common",
            "-l",
            "common",
        ],
        [
            "gh",
            "issue",
            "new",
            "-t",
            "Another issue to submit",
            "-b",
            "",
            "-a",
            "@me",
            "-l",
            "issue",
        ],
    ]


@test("issues are submitted when --dry-run is not passed, with gitlab provider")
def _(_=setup, opts=default_opts):
    Issue._get_remote_url = Mock(
        return_value=urlparse("https://gitlab.com/ewen-lbh/gh-api-playground")
    )
    run(opts=opts | {"<file>": "test_some_issues"})
    assert [call.args[0] for call in subprocess.run.mock_calls] == [
        [
            "glab",
            "issue",
            "new",
            "-t",
            "An issue to submit",
            "-d",
            "",
            "-a",
            "common",
            "-l",
            "common",
        ],
        [
            "glab",
            "issue",
            "new",
            "-t",
            "Another issue to submit",
            "-d",
            "",
            "-a",
            "@me",
            "-l",
            "issue",
        ],
    ]


@test("issues are not submitted when --dry-run is passed")
def _(_=setup, opts=default_opts):
    run(opts=opts | {"<file>": "test_some_issues", "--dry-run": True})
    assert len(subprocess.run.mock_calls) == 0


@test("issues are not submitted when --dry-run is passed, in interactive mode")
def _(_=setup, opts=default_opts):
    run(
        opts=opts
        | {
            "new": True,
            "--dry-run": True,
            "<words>": ["testing", "~this", "issue", "@me"],
        }
    )
    assert len(subprocess.run.mock_calls) == 0


@test(
    "issues are submitted when --dry-run is not passed, in interactive mode, github provider"
)
def _(_=setup, opts=default_opts):
    run(
        opts=opts
        | {
            "new": True,
            "<words>": ["testing", "~this", "issue", "@me"],
        }
    )
    assert [call.args[0] for call in subprocess.run.mock_calls] == [
        [
            "gh",
            "issue",
            "new",
            "-t",
            "testing this issue",
            "-b",
            "",
            "-a",
            "@me",
            "-l",
            "this",
        ],
    ]


@test(
    "issues are submitted when --dry-run is not passed, in interactive mode, gitlab provider"
)
def _(_=setup, opts=default_opts):
    Issue._get_remote_url = Mock(
        return_value=urlparse("https://gitlab.com/ewen-lbh/gh-api-playground")
    )
    run(
        opts=opts
        | {
            "new": True,
            "<words>": ["testing", "~this", "issue", "@me"],
        }
    )
    assert [call.args[0] for call in subprocess.run.mock_calls] == [
        [
            "glab",
            "issue",
            "new",
            "-t",
            "testing this issue",
            "-d",
            "",
            "-a",
            "@me",
            "-l",
            "this",
        ],
    ]
