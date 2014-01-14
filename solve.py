import copy
import re
import sys

nine_set = set(x+1 for x in xrange(9))

class Board:
    def __init__(self):
        self.board = [[0 for x in xrange(9)] for x in xrange(9)] 

    def set(self, x, y, v):
        self.board[x][y] = v

    def get(self, x, y):
        return self.board[x][y]

    def disp(self):
        for x in xrange(9):
            s = " ".join(str(self.get(x,y)) for y in xrange(9))
            print s

    def is_valid(self):
        for st in self.nine_sets():
            if not st == nine_set:
                return False
        return True

    def nine_sets(self):
        for x in xrange(9):  # rows
            yield set(self.board[x])
        for y in xrange(9):  # cols
            yield set(self.board[x][y] for x in xrange(9))
        for x in xrange(3):
            for y in xrange(3):
                o_x = 3*x
                o_y = 3*y
                s = set(self.board[o_x][o_y:o_y+3])
                s.update(self.board[o_x+1][o_y:o_y+3])
                s.update(self.board[o_x+2][o_y:o_y+3])
                yield s

    def start(self):
        self.known = copy.deepcopy(self)
        for x in xrange(9):
            for y in xrange(9):
                if self.get(x, y) == 0:
                    self.set(x, y, 1)
        self.opts = copy.deepcopy(self.board)
        for x in xrange(9):
            for y in xrange(9):
                self.opts[x][y] = nine_set - self.conflicts(x, y)
                if len(self.opts[x][y]) == 1:
                    self.set(x, y, self.opts[x][y].pop())
                    self.known.set(x, y, self.get(x, y))

    def increment(self):
        self.incr_one(0,0)

    def next_xy(self, x, y):
        next_x, next_y = (1, y+1) if x == 8 else (x+1, y)
        if next_y >= 9:
            return (None, None)
        while self.known.get(next_x, next_y) != 0:
            next_x, next_y = (1, y+1) if x == 8 else (x+1, y)
            if next_y >= 9:
                return (None, None)
        return (next_x, next_y)

    def conflicts(self, x, y):
        """Returns a set containing all of the known conflicts that a certain
        cell has."""
        col = set(self.get(i, y) if self.known.get(i,y) != 0 else 0 for i in xrange(9))
        row = set(self.get(x, i) if self.known.get(x,i) != 0 else 0 for i in xrange(9))
        o_x = (x / 3) * 3
        o_y = (y / 3) * 3
        s = set(self.board[o_x][o_y:o_y+3])
        s.update(self.board[o_x+1][o_y:o_y+3])
        s.update(self.board[o_x+2][o_y:o_y+3])
        s.update(col)
        s.update(row)
        return s

    def incr_one(self, x, y):
        next_x, next_y = self.next_xy(x, y)
        if next_x is None:
            self.set(x, y, self.get(x, y)+1)
            return
        self.incr_one(next_x, next_y)
        if self.get(next_x, next_y) >= 10:
            self.set(next_x, next_y, 1)
            new_val = self.get(x, y)+1
            while new_val in self.opts[x][y]:
                new_val += 1
            self.set(x, y, new_val)

class BoardParser:
    def __init__(self, pattern):
        """Sets up the parser with the format string. The string should specify
        the format of a single line. Use _ in place of where the numbers will
        be."""
        esc_pat = re.escape(pattern)
        re_pattern = esc_pat.replace("\_", "(.)")
        self.re = re.compile(re_pattern)

    def parse(self, lines):
        b = Board()
        y = 0
        for line in lines:
            res = self.re.match(line)
            if res is None:
                continue
            for n in xrange(9):
                v = res.group(n+1)
                v = 0 if v is " " else int(v)
                b.set(n, y, v)
            y += 1
        return b

class Solver:
    def __init__(self, board):
        self.board = board
        self.board.start()
    
    def next_solution(self):
        while not self.board.is_valid():
            if self.board.get(0, 0) == 10:
                return None
            self.board.increment()
        soln = copy.deepcopy(self.board)
        self.board.increment()
        return soln

def main():
    lines = sys.stdin.readlines()
    bp = BoardParser("| _ _ _ | _ _ _ | _ _ _ |")
    b = bp.parse(lines)
    solver = Solver(b)
    n_solns = 0
    soln = solver.next_solution()
    while soln is not None:
        n_solns += 1
        soln.disp()
        soln = solver.next_solution()
    print "% solution(s) found" % n_solns


if __name__ == "__main__":
    main()
