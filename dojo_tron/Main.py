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

class Direction:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()

UP=Direction("UP")
DOWN=Direction("DOWN")
LEFT=Direction("LEFT")
RIGHT=Direction("RIGHT")
ALL = {UP, DOWN, RIGHT, LEFT}

class Grid:
    def __init__(self):
        self.grid = [ [0 for y in range(20)] for x in range(30)]

    def move(self,x,y):
        self.grid[x][y] = 1

    def free(self, x, y):
        directions = {UP,DOWN,RIGHT,LEFT}
        if x <= 0 or self.grid[x-1][y]:
            directions.remove(LEFT)
            trace("REMOVE LEFT")
        if x >= 29 or self.grid[x+1][y]:
            directions.remove(RIGHT)
            trace("REMOVE RIGHT")
        if y <= 0 or self.grid[x][y-1]:
            directions.remove(UP)
            trace("REMOVE UP")
        if y >= 19 or self.grid[x][y+1]:
            directions.remove(DOWN)
            trace("REMOVE DOWN")

        trace("Avalaible directions : "+str(directions))
        return directions


    def countFreeCells(self, x, y, dir):
        cellCount=0
        if dir == RIGHT:
            while self.isFree(x+1, y):
                cellCount+=1
                x+=1
        return cellCount


    def isFree(self,x,y):
        return x<30 and self.grid[x][y]==0


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
            if (i == p):
                ourX = x1
                ourY = y1
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # A single line with UP, DOWN, LEFT or RIGHT
        print(str(positionUsed.free(ourX,ourY).pop()))
        # print("UP")




