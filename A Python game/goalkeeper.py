import pygame

class Goalkeeper:
    def __init__(self, x, y, side="left"):
        self.rect = pygame.Rect(x, y, 20, 100)
        self.color = (0, 255, 255) if side == "left" else (255, 0, 255)
        self.speed = 4
        self.side = side
        self.goal_area = pygame.Rect(x, y - 50, 40, 200)

    def update(self, ball):
        # Only track ball if it's approaching this side
        if (self.side == "left" and ball.rect.centerx < 640) or \
           (self.side == "right" and ball.rect.centerx > 640):
            if ball.rect.centery > self.rect.centery:
                self.rect.y += self.speed
            elif ball.rect.centery < self.rect.centery:
                self.rect.y -= self.speed

        # Clamp goalkeeper within vertical goal area
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 720:
            self.rect.bottom = 720

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
