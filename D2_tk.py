import tkinter as tk
from tkinter.font import Font

from grids import Grid3D


def update():
    for grid in grids:
        grid.update()


class Grid:
    def __init__(self, grid, x_offset, y_offset):
        super().__init__()

        self.grid = grid
        self.boxes = {}
        self.pX = {}
        self.pY = {}

        for y in range(len(self.grid.pX)):
            for x in range(len(self.grid.pX[y])):
                self.pX[x, y] = tk.Button(text="   ", font=font)

                def c(x, y):
                    def f():
                        self.grid.set_pX(x, y)
                        update()

                    return f

                self.pX[x, y].configure(command=c(x, y))
                self.pX[x, y].grid(row=y_offset + y * 2, column=x_offset + x * 2 + 1)

        for y in range(len(self.grid.pY)):
            for x in range(len(self.grid.pY[y])):
                self.pY[x, y] = tk.Button(text="   ", font=font)

                def c(x, y):
                    def f():
                        self.grid.set_pY(x, y)
                        update()

                    return f

                self.pY[x, y].configure(command=c(x, y))

                self.pY[x, y].grid(row=y_offset + y * 2 + 1, column=x_offset + x * 2)

        for y in range(self.grid.y):
            for x in range(self.grid.x):
                self.boxes[x, y] = tk.Label(text=" ")
                self.boxes[x, y].grid(row=y_offset + y * 2 + 1, column=x_offset + x * 2 + 1)

        self.update()

    def update(self):
        for y in range(len(self.grid.pX)):
            for x in range(len(self.grid.pX[y])):
                if self.grid.pX[y, x]:
                    self.pX[x, y].configure(text="━")

        for y in range(len(self.grid.pY)):
            for x in range(len(self.grid.pY[y])):
                if self.grid.pY[y, x]:
                    self.pY[x, y].configure(text="┃")

        for y in range(self.grid.y):
            for x in range(self.grid.x):
                self.boxes[x, y].configure(text="x" if self.grid.is_set(x, y) else " ")

    @property
    def width(self):
        return self.grid.x * 2 + 1

    @property
    def height(self):
        return self.grid.y * 2 + 1


def main():
    global w, font, grids
    w = tk.Tk()
    font = Font(family='monospaced')

    g = Grid3D.new(2, 2, 2)

    a = Grid(g.XY_slice(0), 15, 0)
    b = Grid(g.XY_slice(1), 15, a.height)
    c = Grid(g.XY_slice(2), 15, a.height + b.height)
    d = Grid(g.XZ_slice(0), 0, 0)
    e = Grid(g.XZ_slice(1), 0, 5)
    f = Grid(g.XZ_slice(2), 0, 10)

    grids = a, b, c, d, e, f

    w.mainloop()


if __name__ == "__main__":
    main()
