"""Classes and functions for working with calibration digits."""

from typing import List
from dataclasses import dataclass
import re

@dataclass
class CalibrationDigit:
    """Represents a Digit parsed from a line in the calibration values input file.

    Attributes
    ----------
    value : int
        Numerical value of this digit.
    index : int
        Substring position index representing where this digit is located within the line.
    from_word : bool
        Indicates whether this digit was parsed from a word (e.g. "three") or a number (e.g. "3").
    """

    value: int
    index: int
    from_word: bool


def parse_calibration_digits_from_line(line: str, parse_words: bool) -> List[CalibrationDigit]:
    """Parses the given line and extracts all calibration digits found in it.

    Uses regular expressions to parse the line.
    If `parse_words` is True, the line is scanned for substrings describing digits as words, e.g. "three".
    If `parse_words` is False, non-digit characters are ignored completely during the search.

    Parameters
    ----------
    line : str
        The line to parse.
    parse_words : bool
        Whether to also parse the line for English words representing digits.

    Returns
    -------
    List[CalibrationDigit]
        A list of CalibrationDigits, sorted in ascending order of appearance within the line.
    """

    if not isinstance(line, str):
        raise TypeError(f"Expected input to be of type 'str' but got: '{type(line)}'")

    # Maps subtring regular expressions to their respective numerical value
    digit_regexes = {
        #0: { "numeric": re.compile(r"0"), "word": re.compile(r"zero") },
        1: { "numeric": re.compile(r"1"), "word": re.compile(r"one") },
        2: { "numeric": re.compile(r"2"), "word": re.compile(r"two") },
        3: { "numeric": re.compile(r"3"), "word": re.compile(r"three") },
        4: { "numeric": re.compile(r"4"), "word": re.compile(r"four") },
        5: { "numeric": re.compile(r"5"), "word": re.compile(r"five") },
        6: { "numeric": re.compile(r"6"), "word": re.compile(r"six") },
        7: { "numeric": re.compile(r"7"), "word": re.compile(r"seven") },
        8: { "numeric": re.compile(r"8"), "word": re.compile(r"eight") },
        9: { "numeric": re.compile(r"9"), "word": re.compile(r"nine") }
    }

    calibration_digits: List[CalibrationDigit] = []

    # Populate list, digit by digit
    for digit, regexes in digit_regexes.items():
        numeric_matches = list(regexes["numeric"].finditer(line))
        for match in numeric_matches:
            calibration_digits.append(CalibrationDigit(value=digit, index=match.span()[0], from_word=False))

        if parse_words:
            word_matches = list(regexes["word"].finditer(line))
            for match in word_matches:
                calibration_digits.append(CalibrationDigit(value=digit, index=match.span()[0], from_word=True))

    # Return list, sorted by match indices in ascending order
    return sorted(calibration_digits, key=lambda calibration_digit: calibration_digit.index)
