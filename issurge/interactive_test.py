from unittest.mock import Mock

import pytest

from issurge import interactive
from issurge.parser import Issue


@pytest.mark.parametrize(
    "words, expected",
    [
        ("", Issue()),
        ("a simple test right there", Issue(title="a simple test right there")),
        (
            "@me some ~labels to ~organize issues ~bug",
            Issue(
                title="some labels to organize issues",
                labels={"labels", "organize", "bug"},
                assignees={"me"},
            ),
        ),
        (
            "a %milestone to keep ~track of stuff",
            Issue(
                title="a milestone to keep track of stuff",
                labels={"track"},
                milestone="milestone",
            ),
        ),
    ],
)
def test_create_issue_from_words(words, expected):
    actual = interactive.create_issue(words)
    assert actual == expected


def test_create_issue_from_words_with_description():
    global called_count
    called_count = 0

    def mocked_input(prompt):
        global called_count
        called_count += 1
        return {
            1: "A description",
            2: "",
            3: "Another line",
            4: "With more content",
        }.get(called_count, "")

    interactive.input = Mock(wraps=mocked_input)
    actual = interactive.create_issue("A label with a description following it ~now:")
    expected = Issue(
        title="A label with a description following it",
        labels={"now"},
        description="A description\n\nAnother line\nWith more content",
    )
    assert actual == expected
    assert len(interactive.input.mock_calls) == 6
