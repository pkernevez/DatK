import sys
import math



LEVEL = "DEBUG"


def trace(msg):
    if LEVEL == "DEBUG":
        print(msg, file=sys.stderr)


def traces(msgs):
    if LEVEL == "DEBUG":
        msg = " ".join([str(word) for word in msgs])
        print(msg, file=sys.stderr)

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Grid:
    def __init__(self):
        self.grid = [ [0 for y in range(20)] for x in range(30)]

    def move(self,x,y):
        self.grid[x][y] = 1

if __name__ == '__main__':
    positionUsed = Grid()
    # game loop
    while True:
        # n: total number of players (2 to 4).
        # p: your player number (0 to 3).
        n, p = [int(i) for i in input().split()]
        for i in range(n):
            # x0: starting X coordinate of lightcycle (or -1)
            # y0: starting Y coordinate of lightcycle (or -1)
            # x1: starting X coordinate of lightcycle (can be the same as X0 if you play before this player)
            # y1: starting Y coordinate of lightcycle (can be the same as Y0 if you play before this player)
            x0, y0, x1, y1 = [int(j) for j in input().split()]

            positionUsed.move(x0,y0)
            positionUsed.move(x1,y1)

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # A single line with UP, DOWN, LEFT or RIGHT
        print("LEFT")
        print("UP")




