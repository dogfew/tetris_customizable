import sys
import json

import pygame

from desk import Desk
from cube import Figure, NextCubes


def main(background_color: str, second_color: str, cube_colors: list,
         start_speed: int, max_speed: int, speed_step: int,
         screen_width: int, screen_height: int, margin: int, size: int):
    pygame.init()
    clock = pygame.time.Clock()
    margin = margin // size * size
    screen_width, screen_height = size * screen_width, size * screen_height + margin
    game_screen = pygame.display.set_mode((screen_width, screen_height))
    stats_rect = pygame.rect.Rect((0, 0), (screen_width, margin))
    score = 0

    desk = Desk(screen_width, screen_height, margin)
    figure = Figure(NextCubes(desk, cube_colors, size))
    cubes = NextCubes(desk, cube_colors, size)
    cubes_down_event = pygame.USEREVENT + 1
    pygame.time.set_timer(cubes_down_event, start_speed)

    def change_timer(score_value: int):
        pygame.time.set_timer(cubes_down_event, max(start_speed - score_value * speed_step, max_speed))

    font = pygame.font.SysFont('opensans', size * 4 // 5, True)
    next_cubes_surf = pygame.rect.Rect((150, 0), (margin, margin))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == cubes_down_event:
                figure.update(desk, cubes, cube_colors)
                change_timer(score)
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_a:
                        figure.move_left(desk)
                    case pygame.K_d:
                        figure.move_right(desk)
                    case pygame.K_s:
                        figure.move_down(desk)
                    case pygame.K_q:
                        figure.rot_left(desk)
                    case pygame.K_e:
                        figure.rot_right(desk)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_DOWN]:
            figure.move_down(desk)
        if keys[pygame.K_RIGHT]:
            figure.move_right(desk)
        if keys[pygame.K_LEFT]:
            figure.move_left(desk)

        game_screen.fill(background_color)

        next_surf = font.render(f"NEXT:", True, background_color)

        pygame.draw.rect(game_screen, second_color, stats_rect)
        pygame.draw.rect(game_screen, background_color, next_cubes_surf)

        pygame.draw.rect(game_screen, second_color, next_cubes_surf, 2)
        pygame.draw.rect(game_screen, second_color, next_cubes_surf, 4, 5)

        if screen_width < 400:
            score_surf = font.render(f"{score}", True, background_color)
            game_screen.blit(score_surf, score_surf.get_rect(topleft=(size // 2, size * 2)))
        else:
            score_surf = font.render(f"SCORE: {score}", True, background_color)
            game_screen.blit(score_surf, score_surf.get_rect(topright=(screen_width - size // 2, size // 2)))
        game_screen.blit(next_surf, next_surf.get_rect(topleft=(size // 2, size // 2)))

        figure.draw(game_screen)
        desk.draw(game_screen)
        cubes.draw(game_screen)

        score = desk.check(score)
        desk.update()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    kwargs = json.load(open('config.json'))

    main(**kwargs)
