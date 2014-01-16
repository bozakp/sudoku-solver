# Sudoku Solver

An attempt at a [sudoku](http://en.wikipedia.org/wiki/Sudoku) solver written in
Python.

## Usage

Pass a puzzle in via standard input. The input is expected to be a single line
containing 81 characters. A blank cell can be represented by any character that
isn't a digit 1-9 or a new line.

Ex:

    $ python solver.py < unsolved_puzzle.txt

You can also display a progress percentage while solving the puzzles. The
percentage goes to standard error though, so you'll probably want to catch
standard output in a file.

    $ python solver.py -p < puzzles/random1011.txt > results/random1011.log

## Performance

You can find some sample puzzles in the `puzzles/` directory and see the
results in the `results/` directory.
