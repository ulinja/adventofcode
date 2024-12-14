"""Classes to handle a schematic - i.e. a 2D text matrix of dots, numbers and symbols."""

from typing import List
from string import punctuation as SYMBOLS
from pathlib import Path
import re

class Coordinate:
    """Represents a cartesian coordinate in a 2D text matrix.

    In the text matrix coordinate system, the first line of text has Y-coordinate 0,
    with subsequent lines (going down) having increasing Y-values.
    The first character in a line has X-coordinate 0, with subsequent characters (going right) having
    increasing X-values.

    Attributes
    ----------
    x : int
        X coordinate value.
    y : int
        Y coordinate value.
    """

    def __init__(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Coordinate values must be of type 'int'.")
        if not x >= 0 or not y >= 0:
            raise ValueError("Coordinate values must be >= 0.")

        self.x = x
        self.y = y


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"


    def is_adjacent_to(self, other_coordinate: "Coordinate") -> bool:
        """Checks whether this Coordinate is immediately adjacent to `other_coordinate`.

        The two coordinates are immediately adjacent if the distances between their y-coordinates and
        x-coordinates respectively are <= 1.

        Parameters
        ----------
        other_coordinate : Coordinate
            The coordinate to compare this coordinate to.

        Returns
        -------
        bool
            True if `other_coordinate` is adjacent to this coordinate, and False otherwise.

        Raises
        ------
        ValueError
            If `other_coordinate`'s coordinate values are equal to this coordinate's.
        TypeError
            If `other_coordinate` is not a Coordinate.
        """

        if not isinstance(other_coordinate, Coordinate):
            raise TypeError(f"Expected type 'Coordinate' but got '{type(other_coordinate)}'.")

        if other_coordinate.x == self.x and other_coordinate.y == self.y:
            raise ValueError("Coordinate values are equal to each other.")

        return abs(other_coordinate.x - self.x) <= 1 and abs(other_coordinate.y - self.y) <= 1


class Symbol():
    """Represents a symbol which is located within a Schematic.

    Attributes
    ----------
    value : str
        The character value of this Symbol.
    coordinate : Coordinate
        The Coordinate of this Symbol within the schematic.
    """

    def __init__(self, value: str, coordinate: Coordinate):
        if not isinstance(value, str):
            raise TypeError(f"Expected symbol value to be of type 'str' but got '{type(value)}'.")
        if not len(value) == 1:
            raise ValueError("Symbol value must have length 1.")
        if value not in SYMBOLS:
            raise ValueError(f"Symbol value must be one of {SYMBOLS}.")

        self.value = value
        self.coordinate = coordinate


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value}, coordinate={self.coordinate})"


class Gear(Symbol):
    """Represents a Gear, that is a Symbol whose value is '*', and which is adjacent to exactly two part numbers.

    Attributes
    ----------
    gear_ratio : int
        The product of the two Number values adjacent to this Gear.
    """

    def __init__(self, value: str, coordinate: Coordinate, gear_ratio: int):
        Symbol.__init__(self, value, coordinate)
        self.gear_ratio = gear_ratio


class Number():
    """Represents a number located within a Schematic.

    Since numbers in the schematic can span several columns, their position is characterized by a list
    of coordinates.

    Attributes
    ----------
    value : int
        Integer value of this number.
    coordinates : List[Coordinate]
        Coordinates which this number occupies in the schematic.
    """

    def __init__(self, value: int, coordinates: List[Coordinate]):
        if not isinstance(value, int):
            raise TypeError(f"Expected number value to be of type 'int' but got '{type(value)}'.")
        if not value >= 0:
            raise ValueError("Number value must be positive.")

        for coordinate in coordinates:
            if not isinstance(coordinate, Coordinate):
                raise TypeError(f"Expected items of number coordinate list to be of type 'Coordinate' but got '{type(coordinate)}'.")

        self.value = value
        self.coordinates = coordinates

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value}, coordinates={self.coordinates})"


    def is_adjacent_to(self, other_coordinate: Coordinate) -> bool:
        """Compares this Number to the specified coordinate and checks for adjacency.

        If any of this Numbers' coordinates are directly adjacent to `other_coordinate`, returns
        True. If not, returns False.

        Parameters
        ----------
        other_coordinate : Coordinate
            The coordinate to which the adjacency should be checked.

        Returns
        -------
        bool
            True if any of this Numbers' coordinates are adjacent to `other_coordinate`, and False otherwise.
        """

        for coordinate in self.coordinates:
            if coordinate.is_adjacent_to(other_coordinate):
                return True
        return False


class Schematic:
    """Represents a Schematic, a 2D matrix of symbols, dots (empty space) and numbers.

    Attributes
    ----------
    numbers: List[Number]
        A list of all Numbers in this Schematic.
    symbols: List[Symbol]
        A list of all Symbols in this Schematic.
    part_numbers: List[Number]
        A list of all part numbers, that is numbers which are adjacent to a Symbol, in this Schematic.
    gears: List[Gear]
        A list of all Gears in this Schematic.
    """

    def __init__(self, input_file_path: str | Path):
        """Parses a data file containing the Schematic text matrix, and constructs a Schematic from it.

        Parameters
        ----------
        input_file_path : str | Path
            Path to the data file describing this Schematic.

        Raises
        ------
        FileNotFoundError
            If the file pointed to by `input_file_path` does not exist.
        """

        if not isinstance(input_file_path, (str, Path)):
            raise TypeError(f"Expected input file path to be of type 'str' or 'pathlib.Path', but got '{type(input_file_path)}'.")

        input_file_path = Path(input_file_path).resolve().absolute()
        if not input_file_path.is_file():
            raise FileNotFoundError(f"File does not exist: '{input_file_path}'.")

        self.numbers: List[Number] = []
        self.symbols: List[Symbol] = []
        self.part_numbers: List[Number] = []
        self.gears: List[Gear] = []

        lines: List[str] = []
        with open(input_file_path) as input_file:
            lines = input_file.readlines()
        if lines[-1] == "\n":
            lines.pop()

        number_regex = re.compile(r"\d+")
        symbol_regex = re.compile(r"[\!\"\#\$\%\&\'\(\)\*\+\,\-\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]")

        current_y = 0
        for line in lines:
            number_matches = list(number_regex.finditer(line))
            for match in number_matches:
                number_coordinates: List[Coordinate] = []
                for x in range(match.span()[0], match.span()[1]):
                    number_coordinates.append(Coordinate(x=x, y=current_y))
                number_value = int(match.group(0))
                self.numbers.append(Number(value=number_value, coordinates=number_coordinates))

            symbol_matches = list(symbol_regex.finditer(line))
            for match in symbol_matches:
                symbol_coordinate = Coordinate(x=match.span()[0], y=current_y)
                symbol_value = match.group(0)
                self.symbols.append(Symbol(value=symbol_value, coordinate=symbol_coordinate))

            current_y += 1

        for number in self.numbers:
            is_part_number = False
            for symbol in self.symbols:
                if number.is_adjacent_to(symbol.coordinate):
                    is_part_number = True
                    break
            if is_part_number:
                self.part_numbers.append(number)

        for symbol in filter(lambda symbol: symbol.value == "*", self.symbols):
            adjacent_numbers: List[Number] = []
            for number in self.part_numbers:
                if number.is_adjacent_to(symbol.coordinate):
                    adjacent_numbers.append(number)
            if len(adjacent_numbers) == 2:
                gear_ratio = adjacent_numbers[0].value * adjacent_numbers[1].value
                self.gears.append(Gear(value=symbol.value, coordinate=symbol.coordinate, gear_ratio=gear_ratio))
