import pygame

class Ball:
    def __init__(self, x, y):
        self.init_x = x
        self.init_y = y
        self.rect = pygame.Rect(x, y, 20, 20)
        self.color = (255, 255, 255)
        self.vel = [5, 5]

    def update(self, players, goals, score, goalkeepers=[]):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

        # Bounce off top/bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= 720:
            self.vel[1] = -self.vel[1]

        # Bounce off players
        for p in players + goalkeepers:
            if self.rect.colliderect(p.rect):
                self.vel[0] = -self.vel[0]

        # Goal detection
        if self.rect.colliderect(goals["left"]):
            score["right"] += 1
            self.reset()
        elif self.rect.colliderect(goals["right"]):
            score["left"] += 1
            self.reset()

        # Out of bounds on sides (goal kick or throw-in)
        elif self.rect.left < 0 or self.rect.right > 1280:
            self.reset()

    def reset(self):
        self.rect.x = self.init_x
        self.rect.y = self.init_y
        self.vel = [5, 5]

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
