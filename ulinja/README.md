# Advent of Code solutions

This directory contains [my](https://github.com/ulinja/) solvers, written in Python, for Advent Of Code.

**Dependencies:**
- Python >= 3.11

To run a solver for a specific Challenge, run the following:
```bash
cd ulinja
./solve <DAY>
```

For help with the runner:
```bash
./solve -h
```

## Module Structure

Code for the solvers is organized within the `aoc` module.
Each solver provides a module called `main`, with a function called `main`, which runs the solver.
Input data for each challenge is in the `data` directory, and solvers expect to find it there.

```text
ulinja
├── aoc                 # Top level module for sourcecode
│   ├── utils           # Shared utils
│   │   └── file.py
│   └── year23
│       ├── day01
│       │   ├── foo.py  # Code specific to Y23D01
│       │   └── main.py # Solver for Y23D01
│       ├── day02
│       │   ├── bar.py
│       │   └── main.py
│       .
│       .
│       .
├── data                # Directory containing challenge input data
│   ├── 23-01.txt       # My input data for Y23D01
│   ├── 23-02.txt
│   .
│   .
│   .
└── solve               # Main entrypoint to run solvers for challenges
```
