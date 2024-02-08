import pygame
import sys
import random
from datetime import datetime

# Initialize Pygame
pygame.init()

# Set up game window
WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Pong")

background = pygame.image.load('background.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load images
alien_image = pygame.image.load('alien.png')
alien_image = pygame.transform.scale(alien_image, (40, 50))

spaceship_image = pygame.image.load('spaceship.png')
spaceship_image = pygame.transform.scale(spaceship_image, (40, 40))

aircraft_image = pygame.image.load('aircraft.png')

BLOCK_WIDTH, BLOCK_HEIGHT = 80, 60
aircraft_image = pygame.transform.scale(aircraft_image, (BLOCK_WIDTH, BLOCK_HEIGHT))

# Define colors
CYAN = (0, 255, 255)

# Define paddles
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
PADDLE_VELOCITY = 8



class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, direction):
        if direction == "UP" and self.rect.top > 0:
            self.rect.y -= PADDLE_VELOCITY
        elif direction == "DOWN" and self.rect.bottom < HEIGHT:
            self.rect.y += PADDLE_VELOCITY


# Define ball
BALL_RADIUS = 10
BALL_VELOCITY = [5, 5]


class Ball:
    def __init__(self, x, y, velocity):
        self.rect = pygame.Rect(x - BALL_RADIUS, y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.velocity = velocity
        self.last_hit_paddle = None


# Define block
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BLOCK_WIDTH, BLOCK_HEIGHT)


# Define alien
class Alien:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)


# Function to get player names
def get_player_names():
    player1_name = input("Enter name for Player 1: ")
    player2_name = input("Enter name for Player 2: ")
    return player1_name, player2_name


# Set up fonts
SCORE_FONT = pygame.font.Font(None, 36)
WINNER_FONT = pygame.font.Font(None, 60)

# Initialize scores and block reward
player1_score = 0
player2_score = 0
block_reward = 1

# Initialize winner_text
winner_text = ""

# Function to draw game window
def draw_window(player1_paddle, player2_paddle, ball, blocks, alien, player1_score, player2_score, player1_name,
                player2_name, winner_text=None, restart_text=None):
    # Draw background
    WIN.blit(background, (0, 0))

    # Draw the center line
    pygame.draw.line(WIN, CYAN, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    pygame.draw.rect(WIN, CYAN, player1_paddle.rect)
    pygame.draw.rect(WIN, CYAN, player2_paddle.rect)

    # Draw the alien image instead of the spaceship image
    WIN.blit(alien_image, alien.rect.topleft)

    # Draw the spaceship image at the ball's position
    WIN.blit(spaceship_image, (ball.rect.x, ball.rect.y))

    for block in blocks:
        WIN.blit(aircraft_image, block.rect.topleft)  # Change the image here

    player1_score_text = SCORE_FONT.render(f"{player1_name}: {player1_score}", True, CYAN)
    player2_score_text = SCORE_FONT.render(f"{player2_name}: {player2_score}", True, CYAN)

    WIN.blit(player1_score_text, (WIDTH // 4 - player1_score_text.get_width() // 2, 20))
    WIN.blit(player2_score_text, (WIDTH * 3 // 4 - player2_score_text.get_width() // 2, 20))

    if winner_text:
        winner_surface = WINNER_FONT.render(winner_text, True, CYAN)
        WIN.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, 50))

    if restart_text:
        restart_surface = SCORE_FONT.render(restart_text, True, CYAN)
        WIN.blit(restart_surface,
                 (WIDTH // 2 - restart_surface.get_width() // 2, HEIGHT // 2 - restart_surface.get_height() // 2))

    pygame.display.flip()


file = open('external_data_storage.txt', 'a')

# Get player names
player1_name, player2_name = get_player_names()

# Set up paddles, ball, blocks, and alien
player1_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
player2_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball(WIDTH // 2, HEIGHT // 2,
            [random.choice([-1, 1]) * random.uniform(2, 5), random.choice([-1, 1]) * random.uniform(2, 5)])
blocks = [Block(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(2)]
alien = Alien(WIDTH // 2, HEIGHT // 2)  # Initialize alien at the center

# Main game loop
clock = pygame.time.Clock()
run_game = True
game_active = True  # Variable to track whether the game is active or paused
display_restart_text = False  # Variable to track whether to display "Press SPACE to restart"
show_winner = False  # Variable to track whether to display the winner

while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run_game = False
            elif event.key == pygame.K_SPACE and not game_active and show_winner:
                # Restart the game if space is pressed, the game is paused, and the winner is displayed
                player1_score = 0
                player2_score = 0
                blocks = [Block(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(2)]
                game_active = True
                display_restart_text = False
                show_winner = False

    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_paddle.move("UP")
        if keys[pygame.K_s]:
            player1_paddle.move("DOWN")
        if keys[pygame.K_UP]:
            player2_paddle.move("UP")
        if keys[pygame.K_DOWN]:
            player2_paddle.move("DOWN")

        ball.rect.x += ball.velocity[0]
        ball.rect.y += ball.velocity[1]

        # Ball and wall collisions
        if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
            ball.velocity[1] = -ball.velocity[1]

        # Ball and paddle collisions
        if ball.rect.colliderect(player1_paddle.rect):
            ball.velocity[0] = -ball.velocity[0]
            ball.last_hit_paddle = "Player 1"
        elif ball.rect.colliderect(player2_paddle.rect):
            ball.velocity[0] = -ball.velocity[0]
            ball.last_hit_paddle = "Player 2"

        # Ball and block collisions
        for block in blocks:
            if ball.rect.colliderect(block.rect):
                if ball.last_hit_paddle == "Player 1":
                    player1_score += block_reward
                elif ball.last_hit_paddle == "Player 2":
                    player2_score += block_reward
                blocks.remove(block)
                blocks.append(Block(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

        # Ball and alien collisions
        if ball.rect.colliderect(alien.rect):
            if ball.last_hit_paddle == "Player 1":
                player1_score -= 1
            elif ball.last_hit_paddle == "Player 2":
                player2_score -= 1
            alien.rect.x = random.randint(50, WIDTH - 50)
            alien.rect.y = random.randint(50, HEIGHT - 50)

        # Scoring
        if ball.rect.left <= 0:
            player2_score += 1
            ball.rect.x = WIDTH // 2
            ball.rect.y = HEIGHT // 2
        elif ball.rect.right >= WIDTH:
            player1_score += 1
            ball.rect.x = WIDTH // 2
            ball.rect.y = HEIGHT // 2

        # Check for winner
        if player1_score >= 10 or player2_score >= 10 or player1_score == -1 or player2_score == -1:
            if player1_score == -1 or player2_score == -1:
                winner_text = f"{player1_name if player1_score == -1 else player2_name} Loses!"
            else:
                winner_text = f"{player1_name} Wins!" if player1_score >= 10 else f"{player2_name} Wins!"
            show_winner = True
            game_active = False

        if show_winner:
            current_datetime = datetime.now().replace(microsecond=0)
            file.write(
                f'Winner: {winner_text},{player1_name}: {player1_score},{player2_name}: {player2_score}, Date and Time: {current_datetime}\n')

            draw_window(player1_paddle, player2_paddle, ball, blocks, alien, player1_score, player2_score,
                        player1_name, player2_name, winner_text=f"{winner_text} Press SPACE to restart.",
                        restart_text=None)
        else:
            draw_window(player1_paddle, player2_paddle, ball, blocks, alien, player1_score, player2_score,
                        player1_name, player2_name, restart_text=None)

    elif display_restart_text:
        # Display "Press SPACE to restart" only if the game is paused
        draw_window(player1_paddle, player2_paddle, ball, blocks, alien, player1_score, player2_score,
                    player1_name, player2_name, restart_text="Press SPACE to restart.")

    clock.tick(60)

file.close()
pygame.quit()
sys.exit()
