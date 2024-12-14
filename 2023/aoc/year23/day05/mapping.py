"""Classes related to almanac mappings.

The `MapSequence.map()` function is a brute-force solution which takes a long time to run (>= 6 hours).
"""

from typing import List, Tuple
from collections.abc import Callable
import itertools
import math


class SubMap:
    """Represents a submapping as part of a complete mapping, containing a mapping range.

    The range contains all source numbers to which the SubMapping should be applied.
    The map() function applies the mapping to a source number, converting the source number to
    its destination number.

    Attributes
    ----------
    range : Tuple[int, int]
        The minimum and maximum (inclusive) source value for this mapping. Corresponds to the mapping function's domain.
    mapping_function : Callable
        The function which maps values from this SubMap's domain into another integer.
    """

    def __init__(self, destination_range_start: int, source_range_start: int, range_length: int):
        """Constructs a SubMapping."""

        self.range: Tuple[int, int] = (source_range_start, source_range_start + range_length)
        self.mapping_function: Callable[[int], int] = lambda n: n + (destination_range_start - source_range_start)

    def map(self, n: int) -> int:
        if not isinstance(n, int):
            raise TypeError(f"Expected type 'int' as input for mapping function but got '{type(n)}'.")
        if not self.range[0] <= n <= self.range[1]:
            raise ValueError(f"Invalid call to 'map()': input '{n}' is not in range [{self.range[0]}, {self.range[-1]}]")

        return self.mapping_function(n)


class Map:
    """A complete Map which converts an input type into an output type, converting an input number accordingly.

    A Map contains a number of SubMaps. All of a Map's SubMaps combined form a well-defined mapping from the domain
    of all positive integers into the codomain of all positive integers.
    Calling the Map's `map()`-function calculates the function value of an input to this well-defined mapping.

    Attributes
    ----------
    source_type : str
        The source type of this map (e.g. "soil").
    destination_type : str
        The destination type of this map (e.g. "fertilizer").
    submaps : List[]
        The Map's collection of SubMaps.
    """

    def __init__(self, source_type: str, destination_type: str, submaps: List[SubMap]):
        for target_type in [source_type, destination_type]:
            if not isinstance(target_type, str):
                raise TypeError("Expected source and destination types to be of type 'str'.")
        for submap in submaps:
            if not isinstance(submap, SubMap):
                raise TypeError(f"Expected all members of submaps to be of type 'SubMap' but got '{type(submap)}'.")

        self.source_type = source_type
        self.destination_type = destination_type
        self.submaps = submaps

    @staticmethod
    def from_lines(lines: List[str]) -> "Map":
        """Alternate constructor: creates a Map from an input list of strings.

        The lines are expected to be of the following format:
        [
            'light-to-temperature map:\n',
            '45 77 23\n',
            '81 45 19\n',
            '68 64 13\n',
        ]
        """

        source_type = destination_type = ""
        submaps: List[SubMap] = []
        for i, line in enumerate(lines):
            if i == 0:
                source_type, destination_type = line.split(" ")[0].split("-to-")
                continue
            submap_0, submap_1, submap_2 = line.split(" ")
            submaps.append(SubMap(int(submap_0), int(submap_1), int(submap_2)))

        return Map(source_type=source_type, destination_type=destination_type, submaps=submaps)


    def map(self, n: int) -> int:
        for submap in self.submaps:
            if submap.range[0] <= n <= submap.range[1]:
                return submap.map(n)
        return n


class MapSequence:
    """Represents a sequence of Maps.

    seeds : Generator[int]
        Generator containing all seed values.
    min_seed_value : int
        The smallest seed value in the input data.
    max_seed_value : int
        The largest seed value in the input data.
    """

    def __init__(self, input_data_lines: List[str], treat_seeds_as_ranges: bool = False):
        seed_values_str = input_data_lines[0].split("seeds: ")[1].split(" ")
        if not treat_seeds_as_ranges:
            self.seeds = (int(n) for n in seed_values_str)
            self.max_seed_value = max([int(n) for n in seed_values_str])
        else:
            self.seeds = range(0)   # Empty Generator
            self.min_seed_value = math.inf
            self.max_seed_value = 0
            for i in range(0, len(seed_values_str) - 1, 2):
                seed_starting_value = int(seed_values_str[i])
                seed_range_length = int(seed_values_str[i+1])
                self.seeds = itertools.chain(self.seeds, range(seed_starting_value, seed_starting_value + seed_range_length))
                smallest_seed_value = seed_starting_value
                largest_seed_value = seed_starting_value + seed_range_length - 1
                if smallest_seed_value < self.min_seed_value:
                    self.min_seed_value = smallest_seed_value
                if largest_seed_value > self.max_seed_value:
                    self.max_seed_value = largest_seed_value
        del input_data_lines[:2]
        if input_data_lines[-1] == "\n":
            input_data_lines.pop()

        self.maps: List[Map] = []
        map_chunks: List[List[str]] = []
        current_chunk = []
        for line in input_data_lines:
            if line == "\n":
                map_chunks.append(current_chunk)
                current_chunk = []
                continue
            current_chunk.append(line)
        map_chunks.append(current_chunk)
        for chunk in map_chunks:
            self.maps.append(Map.from_lines(chunk))

    def map(self, n: int) -> int:
        result = n
        for map in self.maps:
            result = map.map(result)
        return result

    def get_smallest_location(self) -> int:
        smallest_location = math.inf
        for seed in self.seeds:
            result = self.map(seed)
            if result < smallest_location:
                smallest_location = result
        return int(smallest_location)
