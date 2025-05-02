import os
import webbrowser
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import pytest

import issurge.github
from issurge.main import run
from issurge.parser import Issue, subprocess
from issurge.utils import debugging, dry_running


class MockedSubprocessOutput:
    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout.encode("utf-8")
        self.stderr = stderr.encode("utf-8")


@pytest.fixture
def setup():
    Path("test_empty_issues").write_text("")
    Path("test_some_issues").write_text(
        """~common @common %common
\tAn issue to submit
Another ~issue to submit @me"""
    )
    subprocess.run = Mock(
        return_value=MockedSubprocessOutput(
            "https://github.com/gwennlbh/gh-api-playground/issues/5\n",
            "Some unrelated stuff haha",
        )
    )
    webbrowser.open = Mock()
    Issue._get_remote_url = Mock(
        return_value=urlparse("https://github.com/gwennlbh/gh-api-playground")
    )
    with (
        patch("issurge.github.repo_info") as repo_info,
        patch("issurge.github.available_issue_types") as available_issue_types,
    ):
        repo_info.return_value = issurge.github.OwnerInfo(
            in_organization=True,
            owner="gwennlbh",
            repo="gh-api-playground",
        )
        available_issue_types.return_value = []
        yield
    Path("test_empty_issues").unlink()
    Path("test_some_issues").unlink()
    del os.environ["ISSURGE_DEBUG"]
    del os.environ["ISSURGE_DRY_RUN"]


@pytest.fixture
def default_opts():
    return {
        "<submitter-args>": [],
        "<file>": "test_empty_issues",
        "<words>": [],
        "new": False,
        "--dry-run": False,
        "--debug": False,
        "--open": False,
    }


def test_dry_run_is_set_when_dry_run_is_passed(setup, default_opts):
    run(opts={**default_opts, "--dry-run": True})
    assert dry_running()
    assert not debugging()


def test_debug_is_set_when_debug_is_passed(setup, default_opts):
    run(opts={**default_opts, "--debug": True})
    assert debugging()
    assert not dry_running()


def test_dry_run_and_debug_are_not_set_by_default(setup, default_opts):
    run(opts=default_opts)
    assert not dry_running()
    assert not debugging()


def test_both_dry_run_and_debug_are_set_when_both_are_passed(setup, default_opts):
    run(opts={**default_opts, "--dry-run": True, "--debug": True})
    assert dry_running()
    assert debugging()


def test_issues_are_submitted_when_dry_run_is_not_passed_with_github_provider(
    setup, default_opts
):
    run(opts={**default_opts, "<file>": "test_some_issues"})
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
            "-m",
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


def test_issues_are_submitted_when_dry_run_is_not_passed_with_gitlab_provider(
    setup, default_opts
):
    subprocess.run = Mock(
        return_value=MockedSubprocessOutput(
            "https://gitlab.com/gwennlbh/gh-api-playground/-/issues/5\n",
            "Some unrelated stuff haha",
        )
    )
    Issue._get_remote_url = Mock(
        return_value=urlparse("https://gitlab.com/gwennlbh/gh-api-playground")
    )
    run(opts={**default_opts, "<file>": "test_some_issues"})
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
            "-m",
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


def test_issues_are_not_submitted_when_dry_run_is_passed(setup, default_opts):
    run(opts={**default_opts, "<file>": "test_some_issues", "--dry-run": True})
    assert len(subprocess.run.mock_calls) == 0


def test_issues_are_not_submitted_when_dry_run_is_passed_in_interactive_mode(
    setup, default_opts
):
    run(
        opts={
            **default_opts,
            "new": True,
            "--dry-run": True,
            "<words>": ["testing", "~this", "issue", "@me"],
        }
    )
    assert len(subprocess.run.mock_calls) == 0


def test_issues_are_submitted_when_dry_run_is_not_passed_in_interactive_mode_github_provider(
    setup, default_opts
):
    run(
        opts={
            **default_opts,
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


def test_issues_are_submitted_when_dry_run_is_not_passed_in_interactive_mode_gitlab_provider(
    setup, default_opts
):
    subprocess.run = Mock(
        return_value=MockedSubprocessOutput(
            "https://gitlab.com/gwennlbh/gh-api-playground/-/issues/5\n",
            "Some unrelated stuff haha",
        )
    )
    Issue._get_remote_url = Mock(
        return_value=urlparse("https://gitlab.com/gwennlbh/gh-api-playground")
    )
    run(
        opts={
            **default_opts,
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


def test_issues_are_opened_when_open_is_passed_github_provider(setup, default_opts):
    run(opts={**default_opts, "<file>": "test_some_issues", "--open": True})
    assert [call.args for call in webbrowser.open.mock_calls] == [
        ("https://github.com/gwennlbh/gh-api-playground/issues/5",),
        ("https://github.com/gwennlbh/gh-api-playground/issues/5",),
    ]
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
            "-m",
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


def test_issues_are_opened_when_open_is_passed_gitlab_provider(setup, default_opts):
    subprocess.run = Mock(
        return_value=MockedSubprocessOutput(
            "https://gitlab.com/gwennlbh/gh-api-playground/-/issues/5\n",
            "Some unrelated stuff haha",
        )
    )
    Issue._get_remote_url = Mock(
        return_value=urlparse("https://gitlab.com/gwennlbh/gh-api-playground")
    )
    run(opts={**default_opts, "<file>": "test_some_issues", "--open": True})
    assert [tuple(call.args) for call in webbrowser.open.mock_calls] == [
        ("https://gitlab.com/gwennlbh/gh-api-playground/-/issues/5",),
        ("https://gitlab.com/gwennlbh/gh-api-playground/-/issues/5",),
    ]
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
            "-m",
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


def test_cannot_set_two_issue_types(setup, default_opts):
    with (
        patch("issurge.github.repo_info") as repo_info,
        patch("issurge.github.available_issue_types") as available_issue_types,
    ):
        repo_info.return_value = issurge.github.OwnerInfo(
            in_organization=True,
            owner="gwennlbh",
            repo="gh-api-playground",
        )
        available_issue_types.return_value = ["Bug", "Feature", "Task"]
        with pytest.raises(SystemExit):
            run(
                opts={
                    **default_opts,
                    "<file>": "",
                    "<words>": ["testing", "~this", "~feature", "@me", "~bug"],
                    "new": True,
                }
            )


def test_set_issue_type(setup, default_opts):
    with (
        patch("issurge.github.repo_info") as repo_info,
        patch("issurge.github.available_issue_types") as available_issue_types,
    ):
        repo_info.return_value = issurge.github.OwnerInfo(
            in_organization=True,
            owner="gwennlbh",
            repo="gh-api-playground",
        )
        available_issue_types.return_value = ["Bug", "Feature", "Task"]
        run(
            opts={
                **default_opts,
                "<file>": "",
                "<words>": ["testing", "~this", "~feature", "wow", "@me"],
                "new": True,
            }
        )
    assert [call.args[0] for call in subprocess.run.mock_calls] == [
        [
            "gh",
            "issue",
            "new",
            "-t",
            "testing this feature wow",
            "-b",
            "",
            "-a",
            "@me",
            "-l",
            "this",
        ],
        [
            "gh",
            "api",
            "-X",
            "PATCH",
            "/repos/gwennlbh/gh-api-playground/issues/5",
            "-F",
            "type=Feature",
        ],
    ]
