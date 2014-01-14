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
        for n in xrange(81):
            if not self.valid(n / 9, n % 9):
                return False
        return True

    def valid(self, x, y):
        return self.get_col_set(x) == nine_set and 
                self.get_row_set(y) == nine_set and 
                self.get_sq_set(x, y) == nine_set
        
    def get_col_set(self, x):
        return set(self.board[x][y] for y in xrange(9))

    def get_row_set(self, y):
        return set(self.board[x][y] for x in xrange(9))

    def get_sq_set(self, x, y):
        o_x = (x / 3) * 3
        o_y = (y / 3) * 3
        s = set(self.board[o_x][o_y:o_y+3])
        s.update(self.board[o_x+1][o_y:o_y+3])
        s.update(self.board[o_x+2][o_y:o_y+3])
        return s

    def nine_sets(self):
        for x in xrange(9):  # rows
            yield set(self.board[x])
        for y in xrange(9):  # cols
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
        # for x in xrange(9):
            # for y in xrange(9):
                # if self.get(x, y) == 0:
                    # self.set(x, y, 1)
        self.opts = copy.deepcopy(self.board)
        mult = 1
        for x in xrange(9):
            for y in xrange(9):
                self.opts[x][y] = nine_set - self.conflicts(x, y)
                if len(self.opts[x][y]) == 1 and not self.is_known(x, y):
                    self.set(x, y, self.opts[x][y].pop())
                    self.known.set(x, y, self.get(x, y))
                if not self.is_known(x, y):
                    mult *= len(self.opts[x][y])
        print mult

    def is_known(self, x, y):
        return self.known.get(x, y) != 0

    def increment(self):
        self.incr_one(0,0)

    def permute(self, n):
        next_n = self.next_xy(n)
        if next_n is None:
            yield self
            return
        x = n % 9
        y = n / 9
        next_x = next_n % 9
        next_y = next_n / 9
        for v in self.opts[x][y]:
            self.set(x, y, v)
            for perm in self.permute(next_n):
                yield perm

    def next_xy(self, n):
        next_n = n+1
        if next_n >= 81:
            return None
        next_x = next_n % 9
        next_y = next_n / 9
        while self.is_known(next_x, next_y):
            next_n += 1
            if next_n >= 81:
                return None
            next_x = next_n % 9
            next_y = next_n / 9
        return next_n

    def conflicts(self, x, y):
        """Returns a set containing all of the known conflicts that a certain
        cell has."""
        col = set(self.get(i, y) for i in xrange(9))
        row = set(self.get(x, i) for i in xrange(9))
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
    
    def solutions(self):
        print("%d permutations" % sum(1 for x in self.board.permute(0)))
        return 
        for board in self.board.permute(0):
            if self.board.is_valid():
                yield copy.deepcopy(self.board)

def main():
    lines = sys.stdin.readlines()
    bp = BoardParser("| _ _ _ | _ _ _ | _ _ _ |")
    b = bp.parse(lines)
    solver = Solver(b)
    n_solns = 0
    for soln in solver.solutions():
        soln.disp()
        n_solns += 1
    print "%d solution(s) found" % n_solns


if __name__ == "__main__":
    main()
