from unittest.mock import patch

import pytest

from issurge.github import (
    IssueField,
    available_issue_field_shorthands,
    serialize_body_field,
)


def test_github_serialize_body_field():
    assert serialize_body_field("string", "value") == ["string=value"]

    assert serialize_body_field("number", 42) == ["number=42"]

    assert serialize_body_field("boolean", True) == ["boolean=true"]

    assert serialize_body_field("null", None) == ["null=null"]

    assert serialize_body_field("array", [1, "two"]) == [
        "array[]=1",
        "array[]=two",
    ]

    assert serialize_body_field("object", {"key": "value"}) == ["object[key]=value"]

    assert serialize_body_field(
        "complex", {"list": [1, 2], "dict": {"nested": "yes"}}
    ) == [
        "complex[list][]=1",
        "complex[list][]=2",
        "complex[dict][nested]=yes",
    ]


# Due to available_issue_fields

@pytest.mark.serial
def test_available_issue_field_shorthands():
    with patch("issurge.github.available_issue_fields") as fields:
        fields.return_value = [
            IssueField(
                name="Priority",
                id=0,
                type="single_select",
                options=["Low", "Medium", "High", "Urgent"],
            ),
            IssueField(
                name="Effort",
                id=1,
                type="single_select",
                options=["Low", "Medium", "High"],
            ),
            IssueField(
                name="Impact",
                id=2,
                type="single_select",
                options=["Tah small", "Vla ioudj"],
            ),
        ]

        available = available_issue_field_shorthands()

        assert {s: (f.id, v) for s, (f, v) in available.items()} == {
            "Tah_small": (2, "Tah small"),
            "Vla_ioudj": (2, "Vla ioudj"),
        }
