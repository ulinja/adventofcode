"""Classes representing toy boat races."""

from typing import List, Tuple
import re

from aoc.utils import assertions


class Race:
    """Represents a Race, in which a minimum distance must be covered within a certain duration.

    Attributes
    ----------
    distance_min : int
        Minimum distance in millimeters which must be covered to win this Race.
    duration : int
        Duration of this Race in milliseconds.
    id : int
        ID (sequence number starting at 1) of this Race.
    """

    def __init__(self, id: int,  duration: int, distance_min: int):
        """Constructs a Race."""

        for param_key, param_value in {"id": id, "duration": duration, "distance_min": distance_min}.items():
            if not isinstance(param_value, int):
                raise TypeError(f"Extected type 'int' for parameter '{param_key}' but got '{type(param_value)}'.")
            if not param_value > 0:
                raise ValueError(f"Expected a positive value for parameter '{param_key}' but got '{param_value}'.")

        self.id: int = id
        self.duration: int = duration
        self.distance_min: int = distance_min

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, duration={self.duration}, distance_min={self.distance_min})"

    @staticmethod
    def from_lines(input_lines: List[str], bad_kerning: bool = False) -> List["Race"]:
        """Bulk constructor which parses input data lines into a list of Race objects.

        The `input_lines` are expected to be of the following format:
        [
            "Time:      7  15   30\n",
            "Distance:  9  40  200\n"
        ]

        If `bad_kerning` is set to True, the input lines as listed above are adjusted into this format:
        [
            "Time:      71530\n",
            "Distance:  940200\n"
        ]
        """

        if len(input_lines) != 2:
            raise ValueError("Unexpected number of lines in input: expected 2 lines.")

        number_regex = re.compile(r"\d+")
        durations = [int(match.group(0)) for match in re.finditer(number_regex, input_lines[0])]
        distances = [int(match.group(0)) for match in re.finditer(number_regex, input_lines[1])]
        if len(durations) != len(distances):
            raise RuntimeError("Duration/Distance count mismatch in input data.")

        races: List["Race"] = []

        if bad_kerning:
            race_duration = ""
            for n in durations:
                race_duration += str(n)
            race_distance = ""
            for n in distances:
                race_distance += str(n)
            races.append(Race(1, int(race_duration), int(race_distance)))
        else:
            for id, race_params in enumerate(zip(durations, distances), start=1):
                races.append(Race(id, race_params[0], race_params[1]))

        return races

    def get_distance_by_charge_duration(self, charge_duration: int) -> int:
        """Given a charge duration in milliseconds, returns the race distance covered by a boat in this Race.

        Parameters
        ----------
        charge_duration : int
            The duration in milliseconds of how long the boat is being charged.

        Returns
        -------
        int
            The distance the boat travels in this race given the specified charge duration.
        """

        assertions.is_int_positive_or_zero(charge_duration)

        if charge_duration == 0 or charge_duration >= self.duration:
            return 0
        return (self.duration - charge_duration) * charge_duration

    def is_win_with_charge_duration(self, charge_duration: int) -> bool:
        """Given a charge duration in milliseconds, checks whether this race is won.

        To win a race, the distance covered must exceed the Race's `distance_min`.

        Parameters
        ----------
        charge_duration : int
            The duration in milliseconds of how long the boat is being charged.

        Returns
        -------
        bool
            Whether or not the race is won with the given charge duration.
        """

        return self.get_distance_by_charge_duration(charge_duration) > self.distance_min

    def get_winning_instances(self) -> List[Tuple[int, int]]:
        """Retrieves the list of all winning instances of this race.

        Returns
        -------
        List[Tuple[int, int]]
            A list containing each winning instance of this Race, whereby a winning instance is represented by a Tuple
            of the following format: (charge_diration, distance_covered).
        """

        winning_instances: List[Tuple[int, int]] = []
        for charge_duration in range(1, self.duration):
            if self.is_win_with_charge_duration(charge_duration):
                winning_instances.append((charge_duration, self.get_distance_by_charge_duration(charge_duration)))

        return winning_instances
