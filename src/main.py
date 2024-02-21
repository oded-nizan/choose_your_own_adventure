import pygame
import sys
import os

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Choose Your Own Adventure - Omnibus Forest")

# Load and scale background images
background_images = [
    pygame.image.load(os.path.join('src', 'images', 'background1.jpg')).convert(),
    pygame.image.load(os.path.join('src', 'images', 'background2.jpg')).convert(),
    pygame.image.load(os.path.join('src', 'images', 'background3.jpg')).convert()
]


# Load and scale character image
character_image = pygame.image.load(os.path.join('src', 'images', 'character.png')).convert_alpha()


# Scale down character image
original_character_rect = character_image.get_rect()
character_height = screen_height // 3
scale_factor = character_height / original_character_rect.height
character_image = pygame.transform.scale(character_image, (int(original_character_rect.width * scale_factor),
                                                           int(original_character_rect.height * scale_factor)))

# Set up fonts
font = pygame.font.Font(None, 36)

# Define game states
STATE_START = 0
STATE_STEP1 = 1
STATE_STEP2 = 2
STATE_STEP3 = 3
STATE_STEP4 = 4
STATE_END = 5

# Define transition states
STATE_TRANSITION_OUT = 6
STATE_TRANSITION_IN = 7


# Function to display text
def display_text(text):
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(screen_width // 2, 50))
    screen.blit(text_surface, text_rect)


# Function to fade the screen
def fade_screen():
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill(WHITE)
    for alpha in range(0, 255, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)


# Function to display buttons
def display_buttons(choice1, choice2):
    button_font = pygame.font.Font(None, 24)
    button_width = 200
    button_height = 50
    button_padding = 20
    button_y = 200

    button1_rect = pygame.Rect((screen_width - button_width) // 2, button_y, button_width, button_height)
    button2_rect = pygame.Rect((screen_width - button_width) // 2, button_y + button_height + button_padding,
                               button_width, button_height)

    pygame.draw.rect(screen, WHITE, button1_rect)
    pygame.draw.rect(screen, WHITE, button2_rect)

    button1_text = button_font.render(choice1, True, BLACK)
    button2_text = button_font.render(choice2, True, BLACK)

    screen.blit(button1_text, button1_rect.center)
    screen.blit(button2_text, button2_rect.center)

    return button1_rect, button2_rect


# Main function
def main():
    #  noinspection PyGlobalUndefined
    global choice1_rect, choice2_rect  # Declare as global
    next_state = STATE_START

    # Define game variables
    current_state = STATE_START
    current_background = 0

    # Main loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_state == STATE_START:
                    if choice1_rect.collidepoint(event.pos):
                        current_state = STATE_TRANSITION_OUT
                        next_state = STATE_STEP1
                    elif choice2_rect.collidepoint(event.pos):
                        current_state = STATE_TRANSITION_OUT
                        next_state = STATE_STEP2
                elif current_state == STATE_STEP1:
                    if choice1_rect.collidepoint(event.pos):
                        current_state = STATE_TRANSITION_OUT
                        next_state = STATE_STEP3
                    elif choice2_rect.collidepoint(event.pos):
                        current_state = STATE_TRANSITION_OUT
                        next_state = STATE_STEP4
                elif current_state == STATE_STEP2:
                    if choice1_rect.collidepoint(event.pos):
                        current_state = STATE_TRANSITION_OUT
                        next_state = STATE_STEP4
                    elif choice2_rect.collidepoint(event.pos):
                        current_state = STATE_TRANSITION_OUT
                        next_state = STATE_END
                elif current_state == STATE_STEP3 or current_state == STATE_STEP4:
                    current_state = STATE_TRANSITION_OUT
                    next_state = STATE_START
                elif current_state == STATE_END:
                    if event.button == 1:
                        current_state = STATE_TRANSITION_OUT
                        next_state = STATE_START

        # Update screen
        screen.blit(background_images[current_background], (0, 0))
        if current_state == STATE_START:
            display_text("Welcome to the Omnibus Forest! Choose your path:")
            choice1_rect, choice2_rect = display_buttons("Take the left path", "Take the right path")
        elif current_state == STATE_STEP1:
            display_text("You encounter a river. What do you do?")
            choice1_rect, choice2_rect = display_buttons("Cross the river", "Follow the river downstream")
        elif current_state == STATE_STEP2:
            display_text("You find a hidden cave. Do you enter?")
            choice1_rect, choice2_rect = display_buttons("Enter the cave", "Continue exploring the forest")
        elif current_state == STATE_STEP3:
            display_text("You cross the river and find a treasure chest!")
            choice1_rect, choice2_rect = display_buttons("Return to the forest", "")
        elif current_state == STATE_STEP4:
            display_text("You follow the river and discover a friendly village.")
            choice1_rect, choice2_rect = display_buttons("Stay in the village", "")
        elif current_state == STATE_END:
            display_text("Congratulations! You completed the adventure. Click to restart.")

        if current_state == STATE_TRANSITION_OUT:
            fade_screen()
            current_state = STATE_TRANSITION_IN
            current_background = (current_background + 1) % len(background_images)
        elif current_state == STATE_TRANSITION_IN:
            fade_screen()
            current_state = next_state

        # Blit character image
        character_rect = character_image.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(character_image, character_rect)

        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
