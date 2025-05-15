# pylint: disable=missing-module-docstring

import pytest

from src.utils.string_utils import to_snake_case


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("John Smith", "john_smith"),
        ("once upon a time", "once_upon_a_time"),
        ("Internal_Server_Error", "internal_server_error"),
        ("NOT_FOUND", "not_found"),
        ("some_text", "some_text"),
        ("camelCaseInput", "camelcaseinput"),
        ("PascalCaseInput", "pascalcaseinput"),
    ],
)
def test_to_snake_case(input_str, expected):
    """Test the conversion of various string formats to lower_snake_case."""
    assert to_snake_case(input_str) == expected
