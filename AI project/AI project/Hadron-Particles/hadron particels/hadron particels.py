import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PARTICLE_RADIUS = 10
PARTICLE_COLOR = (255, 255, 255)
PLAYER_RADIUS = 20
PLAYER_COLOR = (0, 255, 0)
AI_COLOR = (255, 0, 0)
TIME_LIMIT = 30  # in seconds
PARTICLE_COUNT = 10  # Default number of particles
PLAYER_SPEED = 5
PARTICLE_SPEED = 5

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hadron Particles")

# Timer
clock = pygame.time.Clock()

# Colors
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)


# Player class
class Player:
    def __init__(self, x, color):
        self.x = x
        self.y = HEIGHT // 2
        self.color = color
        self.score = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), PLAYER_RADIUS)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


# Particle class
class Particle:
    def __init__(self):
        self.x = random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
        self.y = random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)
        self.vx = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
        self.vy = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Bounce off the walls
        if self.x <= PARTICLE_RADIUS or self.x >= WIDTH - PARTICLE_RADIUS:
            self.vx = -self.vx
        if self.y <= PARTICLE_RADIUS or self.y >= HEIGHT - PARTICLE_RADIUS:
            self.vy = -self.vy

    def draw(self):
        pygame.draw.circle(screen, PARTICLE_COLOR, (int(self.x), int(self.y)), PARTICLE_RADIUS)


# Draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# Main menu
def main_menu(result=None):
    click = False
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Hadron Particles', font, TEXT_COLOR, screen, WIDTH // 2, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(WIDTH // 2 - 75, 250, 150, 50)
        button_2 = pygame.Rect(WIDTH // 2 - 75, 310, 150, 50)
        button_3 = pygame.Rect(WIDTH // 2 - 75, 370, 150, 50)
        button_4 = pygame.Rect(WIDTH // 2 - 75, 430, 150, 50)

        buttons = [button_1, button_2, button_3, button_4]
        button_texts = ['Start Game', 'Difficulty', 'Settings', 'Exit']
        actions = [game, difficulty_menu, settings_menu, sys.exit]

        for i, button in enumerate(buttons):
            if button.collidepoint((mx, my)):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button)
                if click and actions[i]:
                    actions[i]()
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, button)

            draw_text(button_texts[i], button_font, TEXT_COLOR, screen, button.centerx, button.centery)

        if result:
            draw_text(f"The winner is {result}!", button_font, TEXT_COLOR, screen, WIDTH // 2, 200)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# Game function
def game():
    start_time = pygame.time.get_ticks()

    # Create players
    player = Player(100, PLAYER_COLOR)
    ai = Player(WIDTH - 100, AI_COLOR)

    # Generate initial particles
    particles = [Particle() for _ in range(PARTICLE_COUNT)]

    ai_dx, ai_dy = random.uniform(-2, 2), random.uniform(-2, 2)
    ai_change_direction_interval = 0.5  # AI changes direction every 0.5 seconds
    last_ai_change_direction_time = start_time / 1000

    running = True
    while running:
        current_time = pygame.time.get_ticks() / 1000

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN]:
            player.move(0, PLAYER_SPEED)
        if keys[pygame.K_LEFT]:
            player.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            player.move(PLAYER_SPEED, 0)

        # AI movement (random, changing direction every ai_change_direction_interval)
        if current_time - last_ai_change_direction_time > ai_change_direction_interval:
            ai_dx, ai_dy = random.uniform(-5, 5), random.uniform(-5, 5)
            last_ai_change_direction_time = current_time

        ai.move(ai_dx, ai_dy)

        # Ensure AI stays within the screen
        ai.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, ai.x))
        ai.y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, ai.y))

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw particles
        for particle in particles:
            particle.move()
            particle.draw()

        # Draw players
        player.draw()
        ai.draw()

        # Display score
        player_score_text = button_font.render(f"Player: {player.score}", True, PLAYER_COLOR)
        ai_score_text = button_font.render(f"AI: {ai.score}", True, AI_COLOR)
        screen.blit(player_score_text, (50, 50))
        screen.blit(ai_score_text, (WIDTH - 150, 50))

        # Check for collisions with particles
        for particle in particles:
            dist_to_player = ((particle.x - player.x) ** 2 + (particle.y - player.y) ** 2) ** 0.5
            dist_to_ai = ((particle.x - ai.x) ** 2 + (particle.y - ai.y) ** 2) ** 0.5
            if dist_to_player <= PLAYER_RADIUS + PARTICLE_RADIUS:
                player.score += 1
                particle.x = random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
                particle.y = random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)
                particle.vx = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
                particle.vy = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
            if dist_to_ai <= PLAYER_RADIUS + PARTICLE_RADIUS:
                ai.score += 1
                particle.x = random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
                particle.y = random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)
                particle.vx = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)
                particle.vy = random.uniform(-PARTICLE_SPEED, PARTICLE_SPEED)

        # Update the display
        pygame.display.flip()

        # Check time limit
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed_time >= TIME_LIMIT:
            running = False

        # Cap the frame rate
        clock.tick(60)

    # Determine the winner
    winner = "Player" if player.score > ai.score else "AI"
    main_menu(result=winner)


# Difficulty menu
def difficulty_menu():
    click = False
    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Select Difficulty', font, TEXT_COLOR, screen, WIDTH // 2, 100)

        mx, my = pygame.mouse.get_pos()

        button_easy = pygame.Rect(WIDTH // 2 - 75, 250, 150, 50)
        button_normal = pygame.Rect(WIDTH // 2 - 75, 310, 150, 50)
        button_hard = pygame.Rect(WIDTH // 2 - 75, 370, 150, 50)
        button_back = pygame.Rect(WIDTH // 2 - 75, 430, 150, 50)

        buttons = [button_easy, button_normal, button_hard, button_back]
        button_texts = ['Easy', 'Normal', 'Hard', 'Back']
        difficulties = [60, 30, 15]  # Corresponding time limits for each difficulty

        for i, button in enumerate(buttons):
            if button.collidepoint((mx, my)):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button)
                if click:
                    if i == 3:  # Back button
                        main_menu()
                    else:
                        global TIME_LIMIT
                        TIME_LIMIT = difficulties[i]
                        main_menu()
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, button)

            draw_text(button_texts[i], button_font, TEXT_COLOR, screen, button.centerx, button.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# Settings menu
def settings_menu():
    click = False
    global PARTICLE_COUNT, PLAYER_SPEED, PARTICLE_SPEED

    while True:
        screen.fill(BACKGROUND_COLOR)
        draw_text('Settings', font, TEXT_COLOR, screen, WIDTH // 2, 100)

        mx, my = pygame.mouse.get_pos()

        button_texts = [
            f'Particles: {PARTICLE_COUNT}',
            f'Player Speed: {PLAYER_SPEED}',
            f'Particle Speed: {PARTICLE_SPEED}',
            'Back'
        ]

        # Calculate button sizes
        button_widths = [button_font.size(text)[0] + 20 for text in button_texts]
        button_height = 50

        buttons = [
            pygame.Rect(WIDTH // 2 - button_widths[0] // 2, 250, button_widths[0], button_height),
            pygame.Rect(WIDTH // 2 - button_widths[1] // 2, 310, button_widths[1], button_height),
            pygame.Rect(WIDTH // 2 - button_widths[2] // 2, 370, button_widths[2], button_height),
            pygame.Rect(WIDTH // 2 - button_widths[3] // 2, 430, button_widths[3], button_height)
        ]

        for i, button in enumerate(buttons):
            if button.collidepoint((mx, my)):
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button)
                if click:
                    if i == 0:  # Adjust particle count
                        PARTICLE_COUNT = (PARTICLE_COUNT + 5) if (
                                                                         PARTICLE_COUNT + 5) <= 50 else 5  # Cycle between 5 and 50
                    elif i == 1:  # Adjust player speed
                        PLAYER_SPEED = (PLAYER_SPEED % 10) + 1  # Cycle between 1 and 10
                    elif i == 2:  # Adjust particle speed
                        PARTICLE_SPEED = (PARTICLE_SPEED % 10) + 1  # Cycle between 1 and 10
                    elif i == 3:  # Back button
                        main_menu()
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, button)

            draw_text(button_texts[i], button_font, TEXT_COLOR, screen, button.centerx, button.centery)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# Run the main menu
main_menu()
