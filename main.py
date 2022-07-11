import sys

import pygame

from board import Board
from cube import Figure, NextCubes
from config import (background_color, second_color, font_size,
                    start_speed, max_speed, speed_step,
                    size, screen_width, screen_height, margin)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    game_screen = pygame.display.set_mode((screen_width, screen_height))
    stats_rect = pygame.rect.Rect((0, 0), (screen_width, margin))
    score = 0

    board = Board()
    figure = Figure(NextCubes(board))
    cubes = NextCubes(board)
    cubes_down_event = pygame.USEREVENT + 1
    pygame.time.set_timer(cubes_down_event, start_speed)

    def change_timer(score_value: int):
        pygame.time.set_timer(cubes_down_event, max(start_speed - score_value * speed_step, max_speed))

    font = pygame.font.SysFont('opensans', font_size, True)
    next_cubes_surf = pygame.rect.Rect((screen_width - size * 4.5 - 10, 0), (4.5 * size, 4.5 * size))

    score_text = "{}"
    score_surf = font.render(score_text, True, background_color)

    score_rect = score_surf.get_rect(topleft=(5, margin // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == cubes_down_event:
                figure.update(board, cubes)
                change_timer(score)
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a | pygame.K_LEFT:
                        figure.move_left(board)
                    case pygame.K_d | pygame.K_RIGHT:
                        figure.move_right(board)
                    case pygame.K_s | pygame.K_DOWN:
                        figure.move_down(board)
                    case pygame.K_q | pygame.K_w | pygame.K_UP:
                        figure.rot_left(board)
                    case pygame.K_e:
                        figure.rot_right(board)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            figure.move_down(board)

        game_screen.fill(background_color)

        pygame.draw.rect(game_screen, second_color, stats_rect)
        pygame.draw.rect(game_screen, background_color, next_cubes_surf)

        pygame.draw.rect(game_screen, second_color, next_cubes_surf, 2)
        pygame.draw.rect(game_screen, second_color, next_cubes_surf, 4, 5)

        score_surf = font.render(score_text.format(score), True, background_color)
        game_screen.blit(score_surf, score_rect)

        figure.draw(game_screen)
        board.draw(game_screen)
        cubes.draw(game_screen)

        score = board.check(score)
        board.update()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
