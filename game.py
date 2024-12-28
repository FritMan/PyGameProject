import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 1500, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Класс игрока
class Player:
    def __init__(self):
        self.image = pygame.image.load('cat2.jpg')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 10

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # Рисуем изображение игрока на экране

    def move(self, dx):
        if 0 <= self.x + dx <= WIDTH - self.width:
            self.x += dx

# Класс врага
class Enemy:
    def __init__(self):
        self.image = pygame.image.load('fish.jpg')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(1, 4)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))  # Рисуем изображение врага на экране

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, WIDTH - self.width)
            self.speed = random.randint(1, 4)

# Основная функция игры
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Избегай врагов!")
    clock = pygame.time.Clock()
    player = Player()
    enemies = [Enemy() for _ in range(5)]

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)

        screen.fill(BLACK)
        player.draw(screen)

        for enemy in enemies:
            enemy.fall()
            enemy.draw(screen)
            # Проверка столкновения
            if (player.x < enemy.x + enemy.width and
                    player.x + player.width > enemy.x and
                    player.y < enemy.y + enemy.height and
                    player.height + player.y > enemy.y):
                run = False

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()