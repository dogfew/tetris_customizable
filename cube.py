import pygame
import numpy as np

from desk import Desk
from random import choice


class Cube(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, color: str, size: int):
        super().__init__()
        self.x, self.y = x, y
        self.size = size
        self.color = color

    def draw(self, screen: pygame.display):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, '#3c3c3c', self.rect, self.size // 10)
        pygame.draw.rect(screen, '#ffffff', self.rect, 1)

    @property
    def rect(self):
        return pygame.rect.Rect(self.x, self.y, self.size, self.size)


class NextCubes(pygame.sprite.Group):
    def __init__(self, desk: Desk, cube_colors: list, size: int):
        super().__init__()
        self.color = choice(cube_colors)
        self.size = size
        self.margin = desk.end
        coords = {(0, 0)}
        while len(coords) < 4:
            base = choice(list(coords))
            if choice([0, 1]):
                new_coords = base[0] + 1, base[1]
            else:
                new_coords = base[0], base[1] + 1
            coords.add(new_coords)
        cubes = [Cube((x + 1) * size, desk.end // size * size + y * size, self.color, size) for x, y in coords]
        self.add(*cubes)

    def draw(self, screen: pygame.display):
        for cube in self:
            rect = (cube.x + 160, cube.y - self.margin + 25, cube.size, cube.size)
            rect = list(i * 40 / cube.size for i in rect)
            pygame.draw.rect(screen, self.color, rect)
            pygame.draw.rect(screen, '#3c3c3c', rect, cube.size // 10)
            pygame.draw.rect(screen, '#ffffff', rect, 1)


class Figure(pygame.sprite.Group):
    def __init__(self, cubes: NextCubes):
        super().__init__()
        self.helper_y = None
        self.helper_x = None
        self.empty()
        self.add(*cubes)
        self.pos = 1
        self.color = cubes.color
        self.size = cubes.size

    def draw(self, screen: pygame.display):
        for cube in self:
            cube.draw(screen)

    def move_left(self, desk: Desk) -> None:
        cubes = [Cube(cube.x, cube.y, self.color, self.size) for cube in self]
        for cube in cubes:
            cube.x -= cube.size
            if pygame.sprite.spritecollideany(cube, desk) or cube.rect.left < 0:
                return
        self.empty()
        self.add(*cubes)

    def move_right(self, desk: Desk) -> None:
        cubes = [Cube(cube.x, cube.y, self.color, self.size) for cube in self]
        for cube in cubes:
            cube.x += cube.size
            if pygame.sprite.spritecollideany(cube, desk) or cube.rect.left >= desk.width:
                return
        self.empty()
        self.add(*cubes)

    def move_down(self, desk: Desk) -> None:
        for cube in self:
            cube.y += cube.size
        if any(cube.y == desk.height for cube in self) or pygame.sprite.groupcollide(desk, self, False, False):
            for cube in self:
                cube.y -= cube.size

    @property
    def helper(self) -> np.array:
        cubes_x = np.array([cube.x // cube.size for cube in self])
        cubes_y = np.array([cube.y // cube.size for cube in self])
        self.helper_x = min(cubes_x)
        self.helper_y = min(cubes_y)
        cubes_x -= self.helper_x
        cubes_y -= self.helper_y
        res = np.zeros((len(cubes_x), len(cubes_y)))
        res[cubes_y, cubes_x] = 1
        return res

    def rot_left(self, desk: Desk) -> None:
        self.pos = (self.pos + 1) % 2
        all_y, all_x = np.nonzero(np.rot90(self.helper, 1))
        new_cubes = []
        for x, y in zip(all_x, all_y):
            cube = Cube((self.helper_x + x) * self.size,
                        (self.helper_y + y - 1 - self.pos) * self.size,
                        self.color, self.size)
            if pygame.sprite.spritecollideany(cube, desk) \
                    or cube.y >= desk.height \
                    or cube.rect.bottom <= desk.end\
                    or cube.rect.left >= desk.width \
                    or cube.rect.left < 0:
                return
            new_cubes.append(cube)
        self.empty()
        self.add(*new_cubes)

    def rot_right(self, desk: Desk) -> None:
        for i in range(3):
            self.rot_left(desk)

    def update(self, desk: Desk, cubes: NextCubes, cube_colors: list) -> None:
        for cube in self:
            cube.y += cube.size
        if any(cube.rect.bottom > desk.height for cube in self) or pygame.sprite.groupcollide(desk, self, False, False):
            for cube in self:
                cube.y -= cube.size
                desk.add(cube)
            self.empty()
            self.__init__(cubes)
            cubes.__init__(desk, cube_colors, self.size)
