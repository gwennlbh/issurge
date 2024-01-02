from ward import test, raises
import os
from .parser import Issue, parse
import textwrap

for fragment, expected, description_expected in [
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
]:

    @test(f"parse {fragment!r}")
    def _(
        fragment=fragment, expected=expected, description_expected=description_expected
    ):
        actual, expecting_description = Issue.parse(fragment)
        assert expecting_description == description_expected
        assert actual == expected


for lines, expected in [
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
]:

    @test(f"parse issues from {textwrap.dedent(lines)!r}")
    def _(lines=lines, expected=expected):
        assert list(parse(lines)) == expected


@test("parse issue with missing description fails")
def _():
    with raises(ValueError) as exception:
        list(parse("An ~issue with a description:\nNo description here"))
    assert (
        str(exception.raised)
        == f"Expected a description after 'An ~issue with a description:'"
    )
