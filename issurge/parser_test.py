from ward import test
from .parser import Issue

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
