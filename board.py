import pygame

from config import size, screen_height, screen_width, margin


class Board(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.width = screen_width
        self.height = screen_height
        self.margin = margin

    def draw(self, screen: pygame.display):
        """Draw all the cubes on the board"""
        for cube in self:
            cube.draw(screen)

    def check(self, score: int) -> int:
        """Verify.
        The condition for the end of the game:
        a cube is placed on the top border of the board.
        Row clearing condition:
        the row is filled with cubes, i.e.
        the number of cubes in a row is equal to the width of the row."""
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
