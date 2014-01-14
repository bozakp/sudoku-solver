import re
import sys

class Board:
    def __init__(self):
        self.board = [[0 for x in xrange(9)] for x in xrange(9)] 

    def set(self, x, y, v):
        self.board[x][y] = v

    def get(self, x, y):
        return self.board[x][y]

    def disp(self):
        for r in self.board:
            print "".join(str(x) for x in r)

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

def main():
    lines = sys.stdin.readlines()
    bp = BoardParser("| _ _ _ | _ _ _ | _ _ _ |")
    b = bp.parse(lines)
    for x in b.board:
        print x

if __name__ == "__main__":
    main()
