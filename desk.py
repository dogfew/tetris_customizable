import pygame


class Desk(pygame.sprite.Group):
    def __init__(self, width, height, end):
        super().__init__()
        self.width = width
        self.height = height
        self.end = end

    def draw(self, screen: pygame.display) -> None:
        for cube in self:
            cube.draw(screen)

    def check(self, score: int) -> int:
        for cube_1 in self:
            bottom = cube_1.rect.bottom
            size = cube_1.size
            if bottom <= self.end + size:
                self.empty()
                return 0
            cubes_line = [cube_2 for cube_2 in self if cube_2.rect.bottom == bottom]
            if len(cubes_line) >= self.width // size:
                score += 1
                self.remove(*cubes_line)
                for cube in self:
                    if cube.rect.bottom <= bottom:
                        cube.y += cube.size
        return score
