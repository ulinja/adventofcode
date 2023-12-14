"""A collection of commonly used assertions."""


def is_int(input_value) -> None:
    """Asserts that the `input_value` is an 'int'.

    Raises
    ------
    TypeError
        If the `input_value` is not of type 'int'.
    """

    if not isinstance(input_value, int):
        raise TypeError(f"Expected type 'int' but got '{type(input_value)}'.")


def is_int_positive_or_zero(input_value) -> None:
    """Asserts that the `input_value` is a non-negative 'int'.

    Raises
    ------
    TypeError
        If the `input_value` is not of type 'int'.
    ValueError
        If the `input_value` is smaller than 0.
    """

    is_int(input_value)
    if input_value < 0:
        raise ValueError(f"Expected a non-negative input value but got '{input_value}'.")


def is_int_positive_non_zero(input_value) -> None:
    """Asserts that the `input_value` is a non-zero, positive 'int'.

    Raises
    ------
    TypeError
        If the `input_value` is not of type 'int'.
    ValueError
        If the `input_value` is smaller than 1.
    """

    is_int(input_value)
    if input_value < 1:
        raise ValueError(f"Expected a positive, non-zero input value but got '{input_value}'.")


def is_string(input_value) -> None:
    """Asserts that the `input_value` is a string.

    Raises
    ------
    TypeError
        If the `input_value` is not of type 'str'.
    """

    if not isinstance(input_value, str):
        raise TypeError(f"Expected type 'str' but got '{type(input_value)}'.")


def is_string_non_empty(input_value) -> None:
    """Asserts that the `input_value` is a non-empty string.

    Raises
    ------
    TypeError
        If the `input_value` is not of type 'str'.
    ValueError
        If the `input_value` is the empty string.
    """

    if not isinstance(input_value, str):
        raise TypeError(f"Expected type 'str' but got '{type(input_value)}'.")
    if len(input_value) < 1:
        raise ValueError(f"Expected input string to be non-empty.")
