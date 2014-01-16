import copy
import re
import sys
import time

nine_set = set(x+1 for x in xrange(9))

class Board:
    def __init__(self):
        self.b = [0 for x in xrange(81)]

    def get(self, n):
        return self.b[n]

    def set(self, n, v):
        self.b[n] = v

    def get_all(self):
        return "".join(str(i) for i in self.b)

    def show(self):
        for y in xrange(9):
            print " ".join(str(x) for x in self.b[9*y:9*y+9])

class Conflicts:
    def __init__(self):
        self.con = [0 for x in xrange(81)]
        for i in xrange(81):
            self.con[i] = Conflicts.gen_conflicts(i)

    @staticmethod
    def gen_conflicts(n):
        """Returns a list of cell indicies which conflict with the given
        cell."""
        x = n % 9
        y = n / 9
        sx = (x / 3) * 3
        sy = (y / 3) * 3
        s1 = set()
        s2 = set()
        s3 = set()
        for i in xrange(9):
            s1.add(x + 9*i)
            s2.add(9*y + i)
            s3.add(9*(sy + i / 3)  + (sx + i % 3))
        s1.remove(n)
        s2.remove(n)
        s3.remove(n)
        return [s1, s2, s3]

    def get_sets(self, n):
        return self.con[n]

    def get(self, n):
        s = set()
        for se in self.con[n]:
            s |= se
        return s


class Options:
    def __init__(self):
        self.sets = [set(nine_set) for x in xrange(81)]

    def get(self, n):
        return self.sets[n]

    def clear(self, n):
        self.sets[n] = None

    def minus(self, n, v):
        if self.sets[n] is None:
            return
        if v in self.sets[n]:
            self.sets[n].remove(v)


class BoardParser:
    def parse(self, line):
        b = Board()
        for i in xrange(len(line)):
            if line[i] in [str(j+1) for j in xrange(9)]:
                b.set(i, int(line[i]))
        return b


class Solver:
    def __init__(self, knowns):
        self.board = Board()
        self.opts = Options()
        self.con = Conflicts()
        for i in xrange(81):
            if knowns.get(i) != 0:
                self.set_known(i, knowns.get(i))

    def set_known(self, n, v):
        self.board.set(n, v)
        self.opts.clear(n)
        for i in self.con.get(n):
            self.opts.minus(i, v)

    def solos(self):
        """Updates the board where there is only one option for a cell.
        Returns None if no cells were updated, otherwise, returns the index
        of one of the cells that was updated"""
        c = None
        for i in xrange(81):
            if self.opts.get(i) is None:
                continue
            if len(self.opts.get(i)) == 1:
                v = self.opts.get(i).pop()
                self.set_known(i, v)
                c = i
        for i in xrange(81):
            if self.opts.get(i) is None:
                continue
            sets = self.con.get_sets(i)
            my_opts = self.opts.get(i)
            for s in sets:
                remaining = set(my_opts)
                for i_cell in s:
                    if self.opts.get(i_cell) is None:
                        v = self.board.get(i_cell)
                        if v in remaining:
                            remaining.remove(v)
                    else:
                        remaining -= self.opts.get(i_cell)
                if len(remaining) == 1:
                    v = remaining.pop()
                    self.set_known(i, v)
                    c = i
        return c

    def all_solos(self):
        while self.solos() is not None:
            pass

    def show(self):
        self.board.show()

    def show_line(self):
        print(self.board.get_all())
    
    def is_valid(self):
        for i in xrange(81):
            s = set(self.board.get(n) for n in self.con.get(i))
            if self.board.get(i) in s:
                return False
        return True

    def permutations(self):
        for p in self.perm(0):
            yield p

    def perm(self, n):
        if self.opts.get(n) is None:
            if n == 80:
                yield self
            else:
                for p in self.perm(n+1):
                    yield p
        else:
            cpy = copy.deepcopy(self)
            for v in self.opts.get(n):
                self.set_known(n, v)
                self.all_solos()
                if n == 80:
                    yield self
                else:
                    for p in self.perm(n+1):
                        yield p
                self.board = copy.deepcopy(cpy.board)
                self.opts = copy.deepcopy(cpy.opts)  # reset the board

    def n_perm(self):
        m = 1
        for i in xrange(81):
            if self.opts.get(i) is not None:
                m *= len(self.opts.get(i))
        return m

def solve_puzzle(line):
    bp = BoardParser()
    b = bp.parse(line)
    solver = Solver(b)
    solver.all_solos()
    c = 0
    for soln in solver.permutations():
        if soln.is_valid():
            soln.show_line()
            c += 1
            break
    return c

def main():
    lines = sys.stdin.readlines()
    s = 0
    for i in xrange(len(lines)):
        start = time.time()
        solve_puzzle(lines[i])
        s += time.time() - start
        sys.stderr.write(str(i)+"\n")
        print("Puzzle: %4d    Time: %7.3f" % (i+1, time.time() - start))
    print("Average time: %f" % (float(s)/len(lines)))

if __name__ == "__main__":
    main()
