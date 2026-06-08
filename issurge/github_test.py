from issurge.github import serialize_body_field


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
