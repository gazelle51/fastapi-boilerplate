"""
Utility functions for string manipulation and formatting.
"""


def to_snake_case(string: str) -> str:
    """Converts a string to `lower_snake_case`.

    Supports strings in `Sentence case`, `Title Case`, `lowercase`, `UPPERCASE` and
    existing `snake_case` formats. Strings in `camelCase` or `PascalCase` will be
    returned as `lowercase` only, not true `snake_case`.

    Args:
        name (str): The string to convert.

    Returns:
        str: The converted string in `lower_snake_case`.
    """
    return string.lower().replace(" ", "_")
