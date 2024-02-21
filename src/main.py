import pygame
import sys
import os

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)

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
background_images = [pygame.transform.scale(bg, (screen_width, screen_height)) for bg in background_images]

# Load and scale character image
character_image = pygame.image.load(os.path.join('src', 'images', 'character.png')).convert_alpha()
character_height = screen_height // 3
original_character_rect = character_image.get_rect()
scale_factor = character_height / original_character_rect.height
character_image = pygame.transform.scale(character_image, (int(original_character_rect.width * scale_factor),
                                                           int(original_character_rect.height * scale_factor)))

# Set up fonts
font = pygame.font.Font(None, 48)

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
def display_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(midtop=(x, y))
    screen.blit(text_surface, text_rect)


# Function to fade the screen
def fade_screen(character_rect, next_state):
    fade_surface = pygame.Surface((screen_width, screen_height))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, 10):
        character_rect.y += 1  # Move character towards the middle of the screen
        screen.blit(background_images[current_background], (0, 0))
        screen.blit(character_image, character_rect)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    # Fade to next scene
    screen.blit(background_images[current_background], (0, 0))
    display_text("Loading...", screen_width // 2, screen_height // 2, color=WHITE)
    pygame.display.flip()
    pygame.time.delay(500)

    # Fade out
    for alpha in range(255, 0, -10):
        screen.blit(background_images[current_background], (0, 0))
        screen.blit(character_image, character_rect)
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

    return next_state


# Function to display buttons
def display_buttons(choice1, choice2):
    button_font = pygame.font.Font(None, 36)
    button_width = 300
    button_height = 100
    button_padding = 40
    button_x = (screen_width - button_width * 2 - button_padding) // 2
    button_y = 400  # Adjusted button position

    button1_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button2_rect = pygame.Rect(button_x + button_width + button_padding, button_y,
                               button_width, button_height)

    pygame.draw.rect(screen, PURPLE, button1_rect)
    pygame.draw.rect(screen, PURPLE, button2_rect)

    button1_text = button_font.render(choice1, True, WHITE)
    button2_text = button_font.render(choice2, True, WHITE)

    button1_text_rect = button1_text.get_rect(center=button1_rect.center)
    button2_text_rect = button2_text.get_rect(center=button2_rect.center)

    screen.blit(button1_text, button1_text_rect)
    screen.blit(button2_text, button2_text_rect)

    return button1_rect, button2_rect


# Main function
def main():
    # noinspection PyGlobalUndefined
    global choice1_rect, choice2_rect, current_background, character_rect  # Declare as global

    # Define game variables
    current_state = STATE_START
    next_state = current_state
    current_background = 0

    # Initialize character rectangle
    character_rect = character_image.get_rect(midbottom=(screen_width // 2, screen_height - 100))

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
            display_text("Welcome to the Omnibus Forest!", screen_width // 2, 150, color=CYAN)
            choice1_rect, choice2_rect = display_buttons("Take the left path", "Take the right path")
        elif current_state == STATE_STEP1:
            display_text("You encounter a river. What do you do?", screen_width // 2, 150, color=CYAN)
            choice1_rect, choice2_rect = display_buttons("Cross the river", "Follow the river downstream")
        elif current_state == STATE_STEP2:
            display_text("You find a hidden cave. Do you enter?", screen_width // 2, 150, color=CYAN)
            choice1_rect, choice2_rect = display_buttons("Enter the cave", "Continue exploring the forest")
        elif current_state == STATE_STEP3:
            display_text("You cross the river and find a treasure chest!", screen_width // 2, 150, color=CYAN)
            choice1_rect, choice2_rect = display_buttons("Return to the forest", "")
        elif current_state == STATE_STEP4:
            display_text("You follow the river and discover a friendly village.", screen_width // 2, 150, color=CYAN)
            choice1_rect, choice2_rect = display_buttons("Stay in the village", "")
        elif current_state == STATE_END:
            display_text("Congratulations! You completed the adventure. Click to restart.", screen_width // 2, 150,
                         color=CYAN)

        if current_state == STATE_TRANSITION_OUT:
            next_state = fade_screen(character_rect, next_state)
            current_background = (current_background + 1) % len(background_images)
            current_state = STATE_TRANSITION_IN

        # Always display buttons
        screen.blit(character_image, character_rect)  # Character is displayed even during transition
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
