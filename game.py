import pygame
import random

pygame.init()

WIDTH, HEIGHT = 1500, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60

class Player:
    def __init__(self):
        self.image = pygame.image.load('cat.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 10
        self.speed = 10
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.facing_right = True

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, dx):
        if 0 <= self.x + dx <= WIDTH - self.width:
            self.x += dx
            self.rect.x = self.x

        if dx > 0 and not self.facing_right:
            self.flip_image()
            self.facing_right = True
        elif dx < 0 and self.facing_right:
            self.flip_image()
            self.facing_right = False

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)


class Fish:
    def __init__(self):
        self.image = pygame.image.load('fish.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = random.randint(1, 4)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def fall(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, WIDTH - self.width)
            self.speed = random.randint(1, 4)
            self.rect.x = self.x


class Bomb:
    def __init__(self, fishes):
        self.image = pygame.image.load('bomb.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        while True:
            self.x = random.randint(0, WIDTH - self.width)
            self.y = random.randint(0, HEIGHT // 2)
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            overlapping = False
            for fish in fishes:
                if self.rect.colliderect(fish.rect):
                    overlapping = True
                    break
            if not overlapping:
                break
        self.speed = random.randint(2, 5)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def fall(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, WIDTH - self.width)
            self.speed = random.randint(2, 5)
            self.rect.x = self.x


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Избегай бомб, лови рыбу!")
    clock = pygame.time.Clock()
    player = Player()
    fishes = [Fish() for _ in range(5)]
    bombs = [Bomb(fishes) for _ in range(3)]
    score = 0
    font = pygame.font.Font(None, 72)
    game_over = False
    game_win = False
    secret_code_entered = False
    secret_code = [pygame.K_3, pygame.K_3, pygame.K_0, pygame.K_1]  # Код - 3,3,0,1
    secret_code_input = []

    def handle_secret_code(key):
        nonlocal secret_code_entered, secret_code_input

        if secret_code_entered:
            return

        if len(secret_code_input) < len(secret_code) and key == secret_code[len(secret_code_input)]:
            secret_code_input.append(key)
            if len(secret_code_input) == len(secret_code):
                secret_code_entered = True
        else:
            secret_code_input = []

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                handle_secret_code(event.key)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-player.speed)
        if keys[pygame.K_RIGHT]:
            player.move(player.speed)

        screen.fill(BLACK)
        player.draw(screen)

        for fish in fishes:
            fish.fall()
            fish.draw(screen)

            if player.rect.colliderect(fish.rect):
                score += 1
                fish.y = -fish.height
                fish.x = random.randint(0, WIDTH - fish.width)
                fish.speed = random.randint(1, 4)
                fish.rect.x = fish.x
                fish.rect.y = fish.y

        for bomb in bombs:
            bomb.fall()
            bomb.draw(screen)

            if player.rect.colliderect(bomb.rect):
                game_over = True

        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        if score >= 20:
            game_win = True

        if game_over:
            screen.fill(BLACK)
            game_over_text = font.render("ВЫ ПРОИГРАЛИ!", True, RED)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            run = False

        if game_win:
            screen.fill(BLACK)
            win_text = font.render("ВЫ ПОБЕДИЛИ!", True, GREEN)
            text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(win_text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)
            run = False

        if secret_code_entered:
            screen.fill(BLACK)
            try:
                rickroll_image = pygame.image.load("secret.png")

                max_size = min(WIDTH, HEIGHT) * 0.6
                image_ratio = rickroll_image.get_width() / rickroll_image.get_height()
                if rickroll_image.get_width() > rickroll_image.get_height():
                  new_width = max_size
                  new_height = max_size / image_ratio
                else:
                  new_width = max_size * image_ratio
                  new_height = max_size

                rickroll_image = pygame.transform.scale(rickroll_image, (int(new_width), int(new_height)))


                image_rect = rickroll_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                screen.blit(rickroll_image, image_rect)

            except pygame.error as e:
                print(f"Ошибка загрузки изображения: {e}")
                screen.blit(font.render("Ошибка загрузки изображения", True, WHITE), (100, 100))
            pygame.display.flip()

            waiting_for_enter = True
            while waiting_for_enter:
              for event in pygame.event.get():
                 if event.type == pygame.KEYDOWN:
                   if event.key == pygame.K_RETURN:
                      waiting_for_enter = False
                      break

            secret_code_entered = False
            secret_code_input = []

    pygame.quit()


if __name__ == '__main__':
    main()