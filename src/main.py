# imports
import pygame
import sys
import os


def main():
    # initialization
    pygame.init()
    # display initialization
    display_width = 1500
    display_height = 1000
    display = pygame.display.set_mode(display_width, display_height)
    pygame.display.set_caption("Choose your own adventure!")

    # load background
    background_image = pygame.image.load(os.path.join('resources', 'background.jpg')).convert()

    # main game loop
    running = True
    while running:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # render display
        display.blit(background_image, (0, 0))
        pygame.display.flip()

    # quit program
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
