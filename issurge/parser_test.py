import textwrap

import pytest

from .parser import Issue, parse


@pytest.mark.parametrize(
    "fragment, expected, description_expected",
    [
        ("", Issue(), False),
        ("a simple test right there", Issue(title="a simple test right there"), False),
        (
            "@me some ~labels to ~organize issues ~bug",
            Issue(
                title="some labels to organize issues",
                labels={"labels", "organize", "bug"},
                assignees={"me"},
            ),
            False,
        ),
        (
            "a %milestone to keep ~track of stuff",
            Issue(
                title="a milestone to keep track of stuff",
                labels={"track"},
                milestone="milestone",
            ),
            False,
        ),
        (
            "A label with a description following it ~now:",
            Issue(title="A label with a description following it", labels={"now"}),
            True,
        ),
        (
            "#.1 An issue with a reference definition",
            Issue(title="An issue with a reference definition", reference=1),
            False,
        ),
    ],
)
def test_parse_fragment(fragment, expected, description_expected):
    actual, expecting_description = Issue.parse(fragment)
    assert expecting_description == description_expected
    assert actual == expected


@pytest.mark.parametrize(
    "lines, expected",
    [
        ("", []),
        ("A simple issue", [Issue(title="A simple issue")]),
        ("~label @me", []),
        (
            """
            @me some ~labels to ~organize issues ~bug
            a %milestone to keep ~track of stuff
            """,
            [
                Issue(
                    title="some labels to organize issues",
                    labels={"labels", "organize", "bug"},
                    assignees={"me"},
                ),
                Issue(
                    title="a milestone to keep track of stuff",
                    labels={"track"},
                    milestone="milestone",
                ),
            ],
        ),
        (
            """
            some stuff
            \tinside: not processed
            """,
            [
                Issue(title="some stuff"),
            ],
        ),
        (
            """
            ~common-tag @someone
            \tright there ~other-tag
            \t//A comment

            \t@someone-else right %here
            """,
            [
                Issue(
                    title="right there",
                    labels={"common-tag", "other-tag"},
                    assignees={"someone"},
                ),
                Issue(
                    title="right",
                    labels={"common-tag"},
                    assignees={"someone-else", "someone"},
                    milestone="here",
                ),
            ],
        ),
        (
            """An ~issue with a description:
\tThis is the %description of the issue:
\t// This is *not* a comment
\tIt has a 
\t- bullet list

\tAnd
\t\tIndentation
            """,
            [
                Issue(
                    title="An issue with a description",
                    labels={"issue"},
                    description="""This is the %description of the issue:
// This is *not* a comment
It has a
- bullet list
And
\tIndentation
""",
                )
            ],
        ),
        (
            """%milestone_test @me
\t~notsure do this
\t~important do that
""",
            [
                Issue(
                    title="do this",
                    labels={"notsure"},
                    assignees={"me"},
                    milestone="milestone_test",
                ),
                Issue(
                    title="do that",
                    labels={"important"},
                    assignees={"me"},
                    milestone="milestone_test",
                ),
            ],
        ),
        (
            """
An issue that references another ~blocked:
\tSee #.1

#.1 The other one ^w^
""",
            [
                Issue(
                    title="An issue that references another",
                    labels={"blocked"},
                    description="See #.1\n",
                ),
                Issue(
                    title="The other one ^w^",
                    reference=1,
                ),
            ],
        ),
        (
            """
Thing:
\tSee issue #.1, #.2
            """,
            [
                Issue(
                    title="Thing",
                    description="See issue #.1, #.2\n",
                )
            ]
        )
    ],
)
def test_parse_issues(lines, expected):
    assert list(parse(textwrap.dedent(lines))) == expected


def test_resolves_references():
    [issue, *_] = list(parse("An issue that references another ~blocked:\n\tSee #.2"))
    assert issue.references == {2}
    issue = issue.resolve_references({2: 1})
    assert issue.description == "See #1\n"

def test_resolves_references_with_commas():
    [issue, *_] = list(parse("An issue that references another ~blocked:\n\tSee #.1, #.2"))
    assert issue.references == {1, 2}
    issue = issue.resolve_references({1: 3, 2: 4})
    assert issue.description == "See #3, #4\n"


def test_splits_sigil():
    assert Issue._word_and_sigil("#.1") == ("#.", "1")


def test_parse_issue_with_missing_description_fails():
    with pytest.raises(
        ValueError, match="Expected a description after 'An ~issue with a description:'"
    ):
        list(parse("An ~issue with a description:\nNo description here"))

