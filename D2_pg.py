import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group

from grids import Grid2D, Grid3D

RES = WIDTH, HEIGHT = 900, 600
FPS = 30
TITLE = 'Dots & Boxes'


class Grid(Sprite):
    background = 'black'
    closed_color = 'white'
    unselected_color = 30, 30, 30
    selected_color = 0, 100, 100
    closed_width = 2
    selectable_width = 10
    half_selectable_width = selectable_width // 2

    offset = offset_x = offset_y = 15
    margin = 10
    length = 100

    multiplier = 2 * margin + length

    @classmethod
    def new(cls, x, y):
        return cls(
            Grid2D.new(x, y),
            Grid2D.new(x, y)
        )

    def __init__(self, selected, closed):
        super().__init__()

        self.selected = selected
        self.closed = closed
        self.dimensions = self.width, self.height = (
            self.multiplier * self.closed.x + 2 * self.offset_x,
            self.multiplier * self.closed.y + 2 * self.offset_y
        )

        self.image = pygame.Surface(self.dimensions)
        self.rect = self.image.get_rect()

        self.selectables_pX = {
            (x, y): (
                self.offset_x + (x * self.multiplier) + self.margin,
                self.offset_y + (y * self.multiplier) - self.half_selectable_width,
                self.offset_x + (x * self.multiplier) + self.margin + self.length,
                self.offset_y + (y * self.multiplier) + self.half_selectable_width
            )
            for y in range(len(self.selected.pX))
            for x in range(len(self.selected.pX[y]))
        }

        self.selectables_pY = {
            (x, y): (
                self.offset_x + (x * self.multiplier) - self.half_selectable_width,
                self.offset_y + (y * self.multiplier) + self.margin,
                self.offset_x + (x * self.multiplier) + self.half_selectable_width,
                self.offset_y + (y * self.multiplier) + self.margin + self.length
            )
            for y in range(len(self.selected.pY))
            for x in range(len(self.selected.pY[y]))
        }

        self.draw()

    def update(self, mouse_x, mouse_y, click):
        if self.rect.x < mouse_x < self.rect.x + self.width:
            if self.rect.y < mouse_y < self.rect.y + self.height:
                for (x, y), (sx, sy, ex, ey) in self.selectables_pX.items():
                    if (self.rect.x + sx) < mouse_x < (self.rect.x + ex):
                        if (self.rect.y + sy) < mouse_y < (self.rect.y + ey):
                            self.selected.set_pX(x, y)

                            if click:
                                self.closed.set_pX(x, y)

                            break
                else:
                    self.selected.pX.fill(0)

                for (x, y), (sx, sy, ex, ey) in self.selectables_pY.items():
                    if (self.rect.x + sx) < mouse_x < (self.rect.x + ex):
                        if (self.rect.y + sy) < mouse_y < (self.rect.y + ey):
                            self.selected.set_pY(x, y)

                            if click:
                                self.closed.set_pY(x, y)

                            break
                else:
                    self.selected.pY.fill(0)

        self.draw()

    def __draw_line(self, start, end, color, width):
        pygame.draw.line(
            self.image,
            color,
            start,
            end,
            width=width
        )

    def __draw_selectable_line(self, start, end, selected, closed):
        self.__draw_line(
            start,
            end,
            self.selected_color if selected else self.unselected_color,
            self.selectable_width
        )

        if closed:
            self.__draw_line(start, end, self.closed_color, self.closed_width)

    def draw(self):
        self.image.fill(self.background)

        for y in range(self.closed.y + 1):
            for x in range(self.closed.x + 1):
                pygame.draw.circle(
                    self.image,
                    self.closed_color,
                    center=(
                        self.offset_x + x * self.multiplier,
                        self.offset_y + y * self.multiplier
                    ),
                    radius=self.closed_width
                )

        for y in range(len(self.closed.pX)):
            for x in range(len(self.closed.pX[y])):
                start = (
                    self.offset_x + (x * self.multiplier) + self.margin,
                    self.offset_y + (y * self.multiplier)
                )

                end = (
                    self.offset_x + (x * self.multiplier) + self.margin + self.length,
                    self.offset_y + (y * self.multiplier)
                )

                self.__draw_selectable_line(start, end, self.selected.pX[y, x], self.closed.pX[y, x])

        for y in range(len(self.closed.pY)):
            for x in range(len(self.closed.pY[y])):
                start = (
                    self.offset_x + (x * self.multiplier),
                    self.offset_y + (y * self.multiplier) + self.margin
                )

                end = (
                    self.offset_x + (x * self.multiplier),
                    self.offset_y + (y * self.multiplier) + self.margin + self.length
                )

                self.__draw_selectable_line(start, end, self.selected.pY[y, x], self.closed.pY[y, x])

        for y in range(self.closed.y):
            for x in range(self.closed.x):
                if self.closed.is_set(x, y):
                    pygame.draw.rect(
                        self.image,
                        self.closed_color,
                        (
                            self.offset_x + (x * self.multiplier) + self.margin,
                            self.offset_y + (y * self.multiplier) + self.margin,
                            self.length,
                            self.length
                        )
                    )


def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    window = pygame.display.set_mode(RES, HWACCEL | HWSURFACE | DOUBLEBUF)
    clock = pygame.time.Clock()

    selected_grid = Grid3D.new(2, 2, 2)
    closed_grid = Grid3D.new(2, 2, 2)

    grid_a = Grid(selected_grid.XY_slice(0), closed_grid.XY_slice(0))
    grid_b = Grid(selected_grid.XY_slice(1), closed_grid.XY_slice(1))
    grid_c = Grid(selected_grid.XY_slice(2), closed_grid.XY_slice(2))

    grid_e = Grid(selected_grid.XZ_slice(0), closed_grid.XZ_slice(0))
    grid_f = Grid(selected_grid.XZ_slice(1), closed_grid.XZ_slice(1))
    grid_g = Grid(selected_grid.XZ_slice(2), closed_grid.XZ_slice(2))

    grids = Group(grid_a, grid_b, grid_c, grid_e, grid_f, grid_g)

    grid_b.rect.x = grid_a.width + 30
    grid_c.rect.x = grid_b.rect.x + grid_b.width + 30

    grid_e.rect.y = grid_a.height + 30
    grid_f.rect.y = grid_a.height + 30
    grid_g.rect.y = grid_a.height + 30

    grid_f.rect.x = grid_e.width + 30
    grid_g.rect.x = grid_f.rect.x + grid_f.width + 30

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    break

        window.fill(Grid.background)

        mouse, click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]

        grids.update(*mouse, click)
        grids.draw(window)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    exit(0)


if __name__ == '__main__':
    main()
