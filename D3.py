from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath

from grids import Grid3D


def line(renderer, a, b, thickness=4):
    lines = LineSegs()
    lines.moveTo(*a)
    lines.drawTo(*b)
    lines.setThickness(thickness)
    # noinspection PyArgumentList
    node = lines.create()
    np = NodePath(node)
    np.reparentTo(renderer)


class Grid(object):
    margin = 1
    length = 8

    multiplier = 2 * margin + length

    def __init__(self, renderer, pos_x, pos_y, pos_z, grid):
        self.renderer = renderer

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z

        self.grid = grid

    def draw(self):
        for z in range(len(self.grid.pX)):
            for y in range(len(self.grid.pX[z])):
                for x in range(len(self.grid.pX[z, y])):
                    if True or self.grid.pX[z, y, x]:
                        line(
                            self.renderer,
                            (
                                self.pos_x + x * self.multiplier + self.margin,
                                self.pos_y + y * self.multiplier,
                                self.pos_z + z * self.multiplier
                            ), (
                                self.pos_x + x * self.multiplier + self.length + self.margin,
                                self.pos_y + y * self.multiplier,
                                self.pos_z + z * self.multiplier
                            ))

        for z in range(len(self.grid.pY)):
            for y in range(len(self.grid.pY[z])):
                for x in range(len(self.grid.pY[z, y])):
                    if True or self.grid.pY[z, y, x]:
                        line(
                            self.renderer,
                            (
                                self.pos_x + x * self.multiplier,
                                self.pos_y + y * self.multiplier + self.margin,
                                self.pos_z + z * self.multiplier
                            ), (
                                self.pos_x + x * self.multiplier,
                                self.pos_y + y * self.multiplier + self.length + self.margin,
                                self.pos_z + z * self.multiplier
                            ))

        for z in range(len(self.grid.pZ)):
            for y in range(len(self.grid.pZ[z])):
                for x in range(len(self.grid.pZ[z, y])):
                    if True or self.grid.pZ[z, y, x]:
                        line(
                            self.renderer,
                            (
                                self.pos_x + x * self.multiplier,
                                self.pos_y + y * self.multiplier,
                                self.pos_z + z * self.multiplier + self.margin
                            ), (
                                self.pos_x + x * self.multiplier,
                                self.pos_y + y * self.multiplier,
                                self.pos_z + z * self.multiplier + self.length + self.margin
                            ))


class DAB(ShowBase):
    def __init__(self):
        super().__init__()

        g = Grid3D.new(2, 2, 2)
        Grid(self.render, -10, -10, -10, g).draw()


def main():
    game = DAB()
    game.run()


if __name__ == '__main__':
    main()
