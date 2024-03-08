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
screen_width = 2550
screen_height = 1440
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
character_height = screen_height // 2.5
original_character_rect = character_image.get_rect()
scale_factor = character_height / original_character_rect.height
character_image = pygame.transform.scale(character_image, (int(original_character_rect.width * scale_factor),
                                                           int(original_character_rect.height * scale_factor)))

# Set up fonts
font = pygame.font.Font(None, 48)

# Define game states
STATE_START = 1
STATE_NEXT = 2
STATE_TO_START = 3
STATE_TO_NEXT = 4

# Define transition states
STATE_TRANSITION_OUT = 6
STATE_TRANSITION_IN = STATE_START

# Define game state's text
START_TEXT = ("You wake up in an ominous forest. To your right you hear barking noises and to your left you see a "
              "pillar of smoke as if it is coming from a campfire. Do you:")
NEXT_TEXT = ("You wake up in an ominous forest with a gold coin in your pocket.  To your right you hear barking "
             "noises and to your left you see a pillar of smoke as if it is coming from a campfire. Do you:")


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


def display_text(text, x, y, color=WHITE, max_width=None):
    words = text.split()
    max_width = max_width or screen_width  # Maximum width for text
    lines = []
    current_line = ''
    word_count = 0
    total_height = 0  # Initialize total height

    for word in words:
        if word_count < 20:  # Change the word count to 10
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
                word_count += 1
            else:
                lines.append(current_line.strip())
                current_line = word
                word_count = 1
        else:
            lines.append(current_line.strip())
            current_line = word
            word_count = 1

    if current_line:
        lines.append(current_line.strip())

    line_height = font.size(" ")[1]  # Height of each line

    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(midtop=(x, y))
        screen.blit(text_surface, text_rect)
        y += line_height  # Move to the next line
        total_height += line_height  # Accumulate total height

    return total_height  # Return the total height after displaying the text


def display_buttons(choice1, choice2, x, y):
    button_font = pygame.font.Font(None, 36)
    button_width = 600
    button_padding = 40
    button_x = (screen_width - button_width * 2 - button_padding) // 2
    button_y = y + 50  # Adjusted button y position to give space between regular text and buttons

    # Render button texts with word wrapping (adjust the words_per_line parameter)
    button1_texts = wrap_text(choice1, 5)  # Adjust the maximum line length
    button2_texts = wrap_text(choice2, 5)

    button1_height = len(button1_texts) * (
            button_font.size(" ")[1] + 5)  # Calculate button height based on text wrapping
    button2_height = len(button2_texts) * (button_font.size(" ")[1] + 5)

    # Set a minimum height for the buttons
    min_button_height = 100  # Set your desired minimum height here

    # Determine the height of the buttons based on the taller button and the minimum height
    button_height = max(min_button_height, max(button1_height, button2_height))

    button1_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    button2_rect = pygame.Rect(button_x + button_width + button_padding, button_y, button_width, button_height)

    pygame.draw.rect(screen, PURPLE, button1_rect, border_radius=10)  # Set the border radius for rounded corners
    pygame.draw.rect(screen, PURPLE, button2_rect, border_radius=10)

    render_text(button1_texts, button1_rect, button_font, WHITE, offset_y=10)  # Adjusted text position
    render_text(button2_texts, button2_rect, button_font, WHITE, offset_y=10)  # Adjusted text position

    return button1_rect, button2_rect, button_height  # Return the button heights


def wrap_text(text, words_per_line):
    words = text.split()
    wrapped_text = [' '.join(words[i:i + words_per_line]) for i in range(0, len(words), words_per_line)]
    return wrapped_text


def render_text(text_lines, button_rect, font, color, offset_y=0):  # Added an offset_y parameter
    line_height = font.size(" ")[1]
    y = button_rect.y
    total_height = 0  # Initialize total height
    for line in text_lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect(
            center=(button_rect.centerx, y + line_height // 2 + offset_y))  # Added offset_y
        screen.blit(text_surface, text_rect)
        y += line_height + 5  # Add some vertical spacing between lines
        total_height += line_height + 5  # Accumulate total height including spacing
    return total_height  # Return the total height of rendered text


# Main function
def main():
    # noinspection PyGlobalUndefined
    global choice1_rect, choice2_rect, current_background, character_rect  # Declare as global

    # Define game variables
    current_state = 1
    next_state = current_state * 10 + 1
    current_background = 0
    current_text = START_TEXT

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
                # Updated section
                match current_state:
                    case 1:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You walk towards the noises and see an old man and a pack of wolves.  Do "
                                            "you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 2
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You walk towards the smoke and see a dying campfire with someone’s "
                                            "belongings around it. Do you:")
                    case 11:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You walk towards the old man and tell him that you really need his help. "
                                            "He agrees to help you but only after you help him get back his daughter "
                                            "who is a little goth girl that ran away from home and is hanging out "
                                            "with a group of bandits. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 2
                            current_state = STATE_TRANSITION_OUT
                            current_text = "You start running towards him but the wolves jump you and knock you out…"
                    case 12:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You start taking all their stuff when a group of five big guys jump from "
                                            "the bushes and threaten you. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 2
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You look around calling “come out wherever you are” and a little goth girl"
                                            "with pig tails comes out from the bushes and asks for her stuff back. Do "
                                            "you:")
                    case 112:
                        next_state = STATE_TO_START
                        current_state = STATE_TRANSITION_OUT
                        current_text = "You start running towards him but the wolves jump you and knock you out…"
                    case 111:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = 12
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("He tells you about the group so you start walking towards the place you "
                                            "saw the smoke pillar since that is the only other place you ever saw "
                                            "evidence of other people.")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_START
                            current_state = STATE_TRANSITION_OUT
                            current_text = "He thinks you’re autistic and it’s contagious so he knocks you out..."
                    case 121:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("They say they will only let you live if you will teach them how to "
                                            "skydive without a parachute and they walk you towards a nearby cliff."
                                            "Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_START
                            current_state = STATE_TRANSITION_OUT
                            current_text = "He thinks you’re autistic and it’s contagious so he knocks you out..."
                    case 122:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You give her the stuff back and a group of five big guys jump out from "
                                            "the bushes. They hand you a gold coin and you put it in your pocket. "
                                            "They start begging for you to teach them how to skydive without a "
                                            "parachute. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_START
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("A group of five big guys jump out of the bushes saying that you made a "
                                            "big mistake threatening their champion. They knock you out…")
                    case 1211:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = STATE_TO_START
                            current_state = STATE_TRANSITION_OUT
                            current_text = "You jump and after a short fall you hit the ground getting knocked out…"
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_START
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You start running and one of them tackles you to the ground and you  get "
                                            "knocked out…")
                    case 1221:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = STATE_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You agree to their request, they lead you to a nearby cliff and you jump "
                                            "off, hit the ground and get knocked out…")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_START
                            current_state = STATE_TRANSITION_OUT
                            current_text = "They tell you that’s not an option and knock you out…"
                    case 2:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You walk towards the noises and see an old man and a pack of wolves.  Do "
                                            "you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 2
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You walk towards the smoke and see a dying campfire with someone’s "
                                            "belongings around it. Do you:")
                    case 21:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You walk towards the old man and tell him that you really need his help. "
                                            "He agrees to help you but asks for your gold coin first. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "You start running towards him but the wolves jump you and knock you out…"
                    case 22:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You start taking all their stuff when a group of five big guys jump from "
                                            "the bushes and threaten you. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 2
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You look around calling “come out wherever you are” and a little goth "
                                            "girl with pig tails comes out from the bushes and asks for her stuff "
                                            "back. Do you:")
                    case 211:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("He teaches you how to skydive without a parachute and asks you to go get "
                                            "his little daughter back home. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "He thinks you’re autistic and it’s contagious so he knocks you out..."
                    case 221:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("They say they will only let you live if you will teach them how to "
                                            "skydive without a parachute and they walk you towards a nearby cliff. Do"
                                            " you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "They think you’re autistic and it’s contagious so they knock you out..."
                    case 222:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You give her the stuff back and a group of five big guys jump out from "
                                            "the bushes. They start begging for you to teach them how to skydive "
                                            "without a parachute. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("A group of five big guys jump out of the bushes saying that you made a "
                                            "big mistake threatening their champion. They knock you out…")
                    case 2111:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 1
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You go towards the smoke and see a dying campfire with someone’s "
                                            "belongings around it. Do you:")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "He thinks you're autistic and it's contagious and knocks you out…"
                    case 2211:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "You jump and after a short fall you hit the ground getting knocked out…"
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You start running and one of them tackles you to the ground and you  get "
                                            "knocked out…")
                    case 2221:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "You agree to their request…"
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "They say “sounds like a you problem” and knock you out…"
                    case 21111:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You attempt to steal the stuff but a group of five big guys jumps from "
                                            "the bushes, lynches you and knocks you out…")
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 2
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("You call out “come out come out wherever you are” and a group of five big "
                                            "guys and a little goth girl jump from the bushes and thank you for not "
                                            "stealing their stuff. They start begging you to teach them how to "
                                            "skydive without a parachute. Do you:")
                    case 211112:
                        if choice1_rect.collidepoint(event.pos):
                            next_state = STATE_TO_NEXT
                            current_state = STATE_TRANSITION_OUT
                            current_text = "They get angry, attack you and knock you out."
                        elif choice2_rect.collidepoint(event.pos):
                            next_state = current_state * 10 + 2
                            current_state = STATE_TRANSITION_OUT
                            current_text = ("They lead you to a nearby cliff and pressure you to jump. You jump off "
                                            "and surprisingly you begin to float over to a nearby mountain where you "
                                            "find a bunch of gold. Congratulations you won the game!.")
                    case 3:
                        next_state = STATE_START
                        current_state = STATE_TRANSITION_OUT
                        current_text = START_TEXT
                    case 4:
                        next_state = STATE_NEXT
                        current_state = STATE_TRANSITION_OUT
                        current_text = NEXT_TEXT

        STATE_TRANSITION_IN = next_state

        # Update screen
        screen.blit(background_images[current_background], (0, 0))
        text_height = display_text(current_text, screen_width // 2, 150, color=CYAN)
        match current_state:
            case 1:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Go to your right and explore the noises",
                    "Go to your left and look for a campfire",
                    screen_width // 2, 400 - text_height // 2)
            case 11:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Go towards the old man and tell him that you really need his help.",
                    "Start running towards him but the wolves jump you and knock you out…",
                    screen_width // 2, 400 - text_height // 2)
            case 12:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Start taking all their stuff when a group of five big guys jump from the bushes and threaten you.",
                    "Look around calling “come out wherever you are” and a little goth girl with pig tails comes out "
                    "from"
                    "the bushes and asks for her stuff back.",
                    screen_width // 2, 400 - text_height // 2)
            case 111:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 112:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Start taking all their stuff when a group of five big guys jump from the bushes and threaten you.",
                    "Look around calling “come out wherever you are” and a little goth girl with pig tails comes out "
                    "from"
                    "the bushes and asks for her stuff back.",
                    screen_width // 2, 400 - text_height // 2)
            case 121:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Sample Option 1 Text",
                    "Sample Option 2 Text",
                    screen_width // 2, 400 - text_height // 2)
            case 122:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Sample Option 1 Text",
                    "Sample Option 2 Text",
                    screen_width // 2, 400 - text_height // 2)
            case 1211:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Sample Option 1 Text",
                    "Sample Option 2 Text",
                    screen_width // 2, 400 - text_height // 2)
            case 1221:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Sample Option 1 Text",
                    "Sample Option 2 Text",
                    screen_width // 2, 400 - text_height // 2)
            case 2:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Go to your right and explore the noises",
                    "Go to your left and look for a campfire",
                    screen_width // 2, 400 - text_height // 2)
            case 21:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Go towards the old man and tell him that you really need his help.",
                    "Start running towards him but the wolves jump you and knock you out…",
                    screen_width // 2, 400 - text_height // 2)
            case 22:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Start taking all their stuff when a group of five big guys jump from the bushes and threaten you.",
                    "Look around calling “come out wherever you are” and a little goth girl with pig tails comes out "
                    "from"
                    "the bushes and asks for her stuff back.",
                    screen_width // 2, 400 - text_height // 2)
            case 211:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 221:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 222:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 2111:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 2211:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 2221:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 21111:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)
            case 211112:
                choice1_rect, choice2_rect, button_height = display_buttons(
                    "Option 1 Sample Text",
                    "Option 2 Sample Text",
                    screen_width // 2, 400 - text_height // 2)

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
