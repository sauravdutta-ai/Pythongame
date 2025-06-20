import pygame
from player import Player
from ball import Ball
from goalkeeper import Goalkeeper
import time

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini FIFA Python")
clock = pygame.time.Clock()
FPS = 60

# Font
font = pygame.font.SysFont("Arial", 36)

# Game Timer (2 mins = 120 seconds)
match_duration = 120
start_time = time.time()

# Create 5 players per team
team1 = [Player(x=100, y=100 + i*100) for i in range(5)]
team2 = [Player(x=WIDTH - 140, y=100 + i*100, is_ai=True) for i in range(5)]

# Goalkeepers
goalie1 = Goalkeeper(20, HEIGHT//2 - 50, side="left")
goalie2 = Goalkeeper(WIDTH - 40, HEIGHT//2 - 50, side="right")

# Ball
ball = Ball(x=WIDTH//2, y=HEIGHT//2)

# Goals
goal_width = 20
goal_height = 200
goals = {
    "left": pygame.Rect(0, HEIGHT//2 - goal_height//2, goal_width, goal_height),
    "right": pygame.Rect(WIDTH - goal_width, HEIGHT//2 - goal_height//2, goal_width, goal_height)
}

# Score
score = {"left": 0, "right": 0}

active_player_index = 0


# Game Loop
running = True
while running:
    dt = clock.tick(FPS) / 1000  # Delta time in seconds
    screen.fill((0, 128, 0))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_TAB:
                active_player_index = (active_player_index + 1) % len(team1)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Control the currently active player (team1[active_player_index])
    keys = pygame.key.get_pressed()
    active_player = team1[active_player_index]
    if keys[pygame.K_w]:
        active_player.rect.y -= active_player.speed
    if keys[pygame.K_s]:
        active_player.rect.y += active_player.speed
    if keys[pygame.K_a]:
        active_player.rect.x -= active_player.speed
    if keys[pygame.K_d]:
        active_player.rect.x += active_player.speed

    # Shoot / Pass
    if keys[pygame.K_SPACE]:
        team1[0].shoot(ball)
    if keys[pygame.K_LSHIFT]:
        team1[0].pass_ball(ball)

    # Update all players
    for p in team1:
        p.update()
    for p in team2:
        p.update(ball)
    goalie1.update(ball)
    goalie2.update(ball)
    ball.update(team1 + team2, goals, score, [goalie1, goalie2])

    # Draw all players
    for p in team1 + team2:
        p.draw(screen)
    goalie1.draw(screen)
    goalie2.draw(screen)
    ball.draw(screen)

    # Highlight active player
    pygame.draw.rect(screen, (255, 255, 255), team1[active_player_index].rect, 3)


    # Draw goals
    pygame.draw.rect(screen, (255, 255, 0), goals["left"])
    pygame.draw.rect(screen, (255, 255, 0), goals["right"])

    # Scoreboard
    score_text = font.render(f"{score['left']} : {score['right']}", True, (255, 255, 255))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    # Timer
    elapsed = time.time() - start_time
    time_left = max(0, int(match_duration - elapsed))
    timer_text = font.render(f"Time Left: {time_left}s", True, (255, 255, 255))
    screen.blit(timer_text, (WIDTH - 250, 20))

    if time_left == 0:
        running = False

    # Update screen
    pygame.display.flip()

pygame.quit()
