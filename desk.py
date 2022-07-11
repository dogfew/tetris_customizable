import pygame

from config import size, screen_height, screen_width, margin


class Desk(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.width = screen_width
        self.height = screen_height
        self.margin = margin

    def draw(self, screen: pygame.display):
        for cube in self:
            cube.draw(screen)

    def check(self, score: int) -> int:
        for cube_1 in self:
            bottom = cube_1.rect.bottom
            if bottom <= self.margin + size:
                self.empty()
                return 0
            cubes_line = [cube_2 for cube_2 in self if cube_2.rect.bottom == bottom]
            if len(cubes_line) >= self.width // size:
                score += 1
                self.remove(*cubes_line)
                for cube in self:
                    if cube.rect.bottom <= bottom:
                        cube.y += size
        return score
