# imports
import pygame
import sys
import os

# global variables
resource_folder = 'resources'


def load_character():
    character_images = [
        pygame.image.load(os.path.join(resource_folder, 'character1.jpg')).convert_alpha(),
        pygame.image.load(os.path.join(resource_folder, 'character2.jpg')).convert_alpha()
    ]
    return character_images


def animate_character(display, character_images, character_x, character_y):
    # set up variables for animation
    frame = 0
    animation_speed = 10  # adjust speed as needed
    frame_counter = 0

    # update frame counter
    frame_counter += 1
    if frame_counter >= animation_speed:
        frame = (frame + 1) % len(character_images)
        frame_counter = 0

    # render to display
    display.blit(character_images[frame], (character_x, character_y))


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

    # load character images
    character_images = load_character()
    # save character dimensions
    character_width, character_height = character_images[0].get_size()
    # calculate character position
    character_x = (display_width - character_width) // 2
    character_y = (display_height - character_height) // 2

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

        # render character
        display.blit(character_image1, (character_x, character_y))
        pygame.display.flip()

    # quit program
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
