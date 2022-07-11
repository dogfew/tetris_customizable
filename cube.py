from random import choice

import pygame
import numpy as np

from board import Board
from config import (size, generate_figure,
                    borders_color, background_color, cube_colors,
                    gap, borders)


class Cube(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: str):
        super().__init__()
        self.x, self.y = x, y
        self.color = color

    def draw(self, screen: pygame.display):
        """Draw a cube"""
        pygame.draw.rect(screen, self.color, (self.x, self.y, size, size))
        pygame.draw.rect(screen, borders_color, self.rect, borders)
        pygame.draw.rect(screen, background_color, self.rect, gap)

    @property
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, size, size)


class NextCubes(pygame.sprite.Group):
    def __init__(self, desk: Board):
        super().__init__()

        coords = generate_figure()
        self.color = choice(cube_colors)
        self.margin = desk.margin
        self.display_cubes = [Cube(x * size + desk.width - size * 4.5,
                                   y * size + 10, self.color) for x, y in coords]
        cubes = [Cube(x * size, desk.margin // size * size + y * size, self.color) for x, y in coords]
        self.add(*cubes)

    def draw(self, screen: pygame.display):
        """Draw the following cubes in the space provided"""
        for cube in self.display_cubes:
            cube.draw(screen)


class Figure(pygame.sprite.Group):
    def __init__(self, cubes: NextCubes):
        super().__init__()
        self.helper_y = None
        self.helper_x = None
        self.empty()
        for cube in cubes:
            cube.x += size
            self.add(cube)
        self.pos = 1
        self.color = cubes.color

    def draw(self, screen: pygame.display):
        """Draw all the cubes that make up the figure"""
        for cube in self:
            cube.draw(screen)

    def move_left(self, desk: Board):
        """Shift figure to the left"""
        cubes = [Cube(cube.x, cube.y, self.color)for cube in self]
        for cube in cubes:
            cube.x -= size
            if pygame.sprite.spritecollideany(cube, desk) or cube.rect.left < 0:
                return
        self.empty()
        self.add(*cubes)

    def move_right(self, desk: Board):
        """Shift figure to the right"""
        cubes = [Cube(cube.x, cube.y, self.color) for cube in self]
        for cube in cubes:
            cube.x += size
            if pygame.sprite.spritecollideany(cube, desk) or cube.rect.left >= desk.width:
                return
        self.empty()
        self.add(*cubes)

    def move_down(self, desk: Board):
        """Shifting the figure down. In case of a collision, roll back the shift."""
        for cube in self:
            cube.y += size
        if any(cube.y == desk.height for cube in self) or pygame.sprite.groupcollide(desk, self, False, False):
            for cube in self:
                cube.y -= size

    @property
    def slice(self) -> np.array:
        """Get a slice of a 4x4 shape for figure"""
        cubes_x = np.array([cube.x // size for cube in self])
        cubes_y = np.array([cube.y // size for cube in self])
        self.helper_x = min(cubes_x)
        self.helper_y = min(cubes_y)
        cubes_x -= self.helper_x
        cubes_y -= self.helper_y
        res = np.zeros((len(cubes_x), len(cubes_y)))
        res[cubes_y, cubes_x] = 1
        return res

    def rot_left(self, board: Board):
        """Rotate figure to the left"""
        self.pos = (self.pos + 1) % 2
        all_y, all_x = np.nonzero(np.rot90(self.slice, 1))
        new_cubes = []
        for x, y in zip(all_x, all_y):
            cube = Cube((self.helper_x + x) * size,
                        (self.helper_y + y - 1 - self.pos) * size,
                        self.color)
            if pygame.sprite.spritecollideany(cube, board) \
                    or cube.y >= board.height \
                    or cube.rect.bottom <= board.margin\
                    or cube.rect.left >= board.width \
                    or cube.rect.left < 0:
                return
            new_cubes.append(cube)
        self.empty()
        self.add(*new_cubes)

    def rot_right(self, desk: Board):
        """Rotate figure to the right"""
        for i in range(3):
            self.rot_left(desk)

    def update(self, desk: Board, cubes: NextCubes):
        """Update the figure and check if there is a collision with the board.
        In case of collision, roll back the movement down and place the piece on the board"""
        for cube in self:
            cube.y += size
        if any(cube.rect.bottom > desk.height for cube in self) or pygame.sprite.groupcollide(desk, self, False, False):
            for cube in self:
                cube.y -= size
                desk.add(cube)
            self.empty()
            self.__init__(cubes)
            cubes.__init__(desk)
