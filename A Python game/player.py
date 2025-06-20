import pygame

class Player:
    def __init__(self, x, y, is_ai=False):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.color = (255, 0, 0) if not is_ai else (0, 0, 255)
        self.is_ai = is_ai
        self.speed = 5

    def update(self, ball=None):
        if self.is_ai:
            if ball and ball.rect.centery > self.rect.centery:
                self.rect.y += self.speed
            elif ball and ball.rect.centery < self.rect.centery:
                self.rect.y -= self.speed
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed
        # Clamp within screen boundaries
        self.rect.y = max(0, min(self.rect.y, 720 - self.rect.height))
        self.rect.x = max(0, min(self.rect.x, 1280 - self.rect.width))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def shoot(self, ball):
        if self.rect.colliderect(ball.rect):
            # Shoot toward goal
            direction = 1 if not self.is_ai else -1
            ball.vel = [direction * 10, 0]

    def pass_ball(self, ball):
        if self.rect.colliderect(ball.rect):
            # Pass slightly forward and to a random vertical direction
            direction = 1 if not self.is_ai else -1
            ball.vel = [direction * 6, 3]
