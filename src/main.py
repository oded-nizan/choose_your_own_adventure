# imports
import pygame
import sys
import os

# global variables
resource_folder = 'resources'
# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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
    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Choose your own adventure!")

    # Set up fonts
    font = pygame.font.Font(None, 36)

    # Define game states
    state_start = 0
    state_room1 = 1
    state_room2 = 2
    state_end = 3
    # Define game variables
    current_state = state_start

    # load background
    background_image = pygame.image.load(os.path.join('resources', 'background.jpg')).convert()

    # load character images
    character_images = load_character()
    # save character dimensions
    character_width, character_height = character_images[0].get_size()
    # calculate character position
    character_x = (display_width - character_width) // 2
    character_y = (display_height - character_height) // 2

    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if current_state == state_start:
                    current_state = state_room1

                elif current_state == state_room1:
                    if event.key == pygame.K_LEFT:
                        current_state = state_room2

                    elif event.key == pygame.K_RIGHT:
                        current_state = state_end

                elif current_state == state_room2:
                    if event.key == pygame.K_RIGHT:
                        current_state = state_room1

                    elif event.key == pygame.K_LEFT:
                        current_state = state_end

                elif current_state == state_end:
                    if event.key == pygame.K_SPACE:
                        current_state = state_start

        # Update display
        display.fill(WHITE)
        if current_state == state_start:
            text = font.render("You wake up in a mysterious room. Press any key to continue.", True, BLACK)
            display.blit(text, (50, 50))
        elif current_state == state_room1:
            text = font.render("You enter room 1. Which way do you go? (Left/Right)", True, BLACK)
            display.blit(text, (50, 50))
        elif current_state == state_room2:
            text = font.render("You enter room 2. Which way do you go? (Left/Right)", True, BLACK)
            display.blit(text, (50, 50))
        elif current_state == state_end:
            text = font.render("You reached the end. Press space to restart.", True, BLACK)
            display.blit(text, (50, 50))

        # Update display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
