"""Classes related to Games in the AOC Y23D02 challenge."""


class Game():
    """Represents a Game.

    Attributes
    ----------
    red_count_min : int
        Highest number of red cubes revealed while this Game was played.
    green_count_min : int
        Highest number of green cubes revealed while this Game was played.
    blue_count_min : int
        Highest number of blue cubes revealed while this Game was played.
    """

    def __init__(self, line: str):
        """Constructs a Game from a line of text input.

        The input line is expected to have the following format:
        `Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green`

        This function splits the input line into tokens to parse the Game data.
        """

        if not isinstance(line, str):
            raise TypeError(f"Expected type 'str' as input, but got '{type(line)}'.")

        if line.endswith("\n"):
            line = line[0:-1]

        self.id = int(line.split(":")[0][5:])

        reveal_tokens = line.split(":")[1][1:].split("; ")

        self.red_count_min = self.green_count_min = self.blue_count_min = 0

        for reveal_token in reveal_tokens:
            count_tokens = reveal_token.split(", ")
            for count_token in count_tokens:
                count = int(count_token.split(" ")[0])
                color = count_token.split(" ")[1]
                if color == "red" and count > self.red_count_min:
                    self.red_count_min = count
                elif color == "green" and count > self.green_count_min:
                    self.green_count_min = count
                elif color == "blue" and count > self.blue_count_min:
                    self.blue_count_min = count

    def possible_with(self, red_max_count: int, green_max_count: int, blue_max_count: int) -> bool:
        """Determines if this game would have been possible if the specified maximum cube counts are assumed.

        If, for any color, the minimum number of revealed cubes is higher than that color's specified maxiumum,
        False is returned. If this is not the case, for all colors, True is returned.

        Returns
        -------
        bool
            Whether or not this Game is possible given the supplied maxima.
        """

        red_possible = self.red_count_min <= red_max_count
        green_possible = self.green_count_min <= green_max_count
        blue_possible = self.blue_count_min <= blue_max_count

        return red_possible and green_possible and blue_possible

    @property
    def power(self):
        return self.red_count_min * self.green_count_min * self.blue_count_min
