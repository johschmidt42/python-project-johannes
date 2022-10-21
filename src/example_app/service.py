"""
Provides several sample functions.

The module contains the following functions:

- `foo(a, b)` - Returns the sum of two numbers (int).
- `bar(a)' - Returns a hello message with the input string.

"""


def foo(a: int, b: int) -> int:
    """
    This is a description what the function does.

    Examples:
        >>> foo(a=1, b=2)
        3
        >>> foo(a=4, b=15)
        19

    Args:
        a: This is the first summand
        b: This is the second summand

    Returns:
        The summation of a and b.
    """
    return a + b


def bar(name: str = "Frank Herbert") -> str:
    """
    Says 'Hello' with input.

    Args:
        name: input string

    Returns:
        A 'Hello' message.
    """
    return f"Hello, {name}!"
