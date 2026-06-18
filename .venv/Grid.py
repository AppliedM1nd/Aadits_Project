import sys

import pygame

screen_width = 1000
screen_height = 1000
cell_width = 100

def main(screen_width, screen_height, cell_width):
    window = create_grid(screen_width, screen_height)

    while True:
        draw_grid(window, cell_width, screen_width, screen_height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



def create_grid(screen_width, screen_height):
    window = pygame.display.set_mode((screen_width, screen_height))
    window.fill((0, 0, 0))
    return window

def draw_grid(window, cell_width, screen_width, screen_height):
    for x in range(0, cell_width, screen_width):
        for y in range(0, cell_width, screen_height):
            rect = pygame.Rect(x, y, screen_width, screen_height)
            pygame.draw.rect(window, (255, 255, 255), rect)

main(screen_width, screen_height, cell_width)