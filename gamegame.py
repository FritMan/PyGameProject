## От разработчиков: сердечно просим ничего не изменять, любое несанкционированное
## вмешательство в код игры скорее всего приведёт к поломке!!!

import pygame
import random
import sqlite3

pygame.init()

WIDTH, HEIGHT = 1500, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60


def create_connection():
    conn = sqlite3.connect('ProjectDB')
    return conn


def create_user(conn, name, score, difficulty):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User (Name, Score, Difficult) VALUES (?, ?, ?)", (name, score, difficulty))
    conn.commit()


def get_users_by_difficulty(conn, difficulty):
    cursor = conn.cursor()
    cursor.execute("SELECT Name, Score FROM User WHERE Difficult = ? ORDER BY Score DESC", (difficulty,))
    return cursor.fetchall()


def display_results(screen, results, difficulty, y_offset):
    font = pygame.font.Font(None, 36)
    header_text = font.render(f"Топ игроков - {difficulty} уровень", True, WHITE)
    screen.blit(header_text, (WIDTH // 2 - header_text.get_width() // 2, 50 + y_offset))

    y = 100 + y_offset
    for name, score in results:
        user_text = font.render(f"{name}: {score}", True, WHITE)
        screen.blit(user_text, (WIDTH // 2 - user_text.get_width() // 2, y))
        y += 40


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
    def __init__(self, speed):
        self.image = pygame.image.load('fish.png')
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = random.randint(0, WIDTH - self.width)
        self.y = -self.height
        self.speed = speed
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
    def __init__(self, fishes, speed):
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
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def fall(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > HEIGHT:
            self.y = -self.height
            self.x = random.randint(0, WIDTH - self.width)
            self.rect.x = self.x


def get_user_name(screen):
    font = pygame.font.Font(None, 74)
    input_text = ""
    input_text_render = font.render(f"Введите имя: {input_text}", True, WHITE)
    input_rect = input_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    while True:
        screen.fill(BLACK)
        screen.blit(input_text_render, input_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif len(input_text) < 45 and event.unicode.isalnum() or event.unicode.isspace():
                    input_text += event.unicode
                input_text_render = font.render(f"Введите имя: {input_text}", True, WHITE)
                input_rect = input_text_render.get_rect(center=(WIDTH // 2, HEIGHT // 2))


def menu_screen(screen):
    font = pygame.font.Font(None, 74)
    title_text = font.render("Игра: Избегай бомб, лови рыбу!", True, WHITE)
    start_text = font.render("Нажмите Enter, чтобы начать", True, WHITE)
    exit_text = font.render("Нажмите Esc, чтобы выйти", True, WHITE)
    easy_text = font.render("Нажмите 1 для легкого уровня", True, WHITE)
    medium_text = font.render("Нажмите 2 для среднего уровня", True, WHITE)
    hard_text = font.render("Нажмите 3 для сложного уровня", True, WHITE)

    screen.fill(BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 100))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 150))
    pygame.display.flip()

    difficulty = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if event.key == pygame.K_RETURN:
                    if difficulty is not None:
                        return difficulty
                if event.key == pygame.K_1:
                    difficulty = 'easy'
                if event.key == pygame.K_2:
                    difficulty = 'medium'
                if event.key == pygame.K_3:
                    difficulty = 'hard'


def get_game_params(difficulty):
    if difficulty == 'easy':
        return 1, 2, 3
    elif difficulty == 'medium':
        return 2, 3, 5
    elif difficulty == 'hard':
        return 3, 4, 7
    else:
        return 1, 1, 3


def get_win_score(difficulty):
    if difficulty == 'easy':
        return 20
    elif difficulty == 'medium':
        return 30
    elif difficulty == 'hard':
        return 40
    else:
        return 10


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Избегай бомб, лови рыбу!")
    user_name = get_user_name(screen)
    if user_name is None:
        return
    difficulty = menu_screen(screen)

    if difficulty is None:
        return

    clock = pygame.time.Clock()

    fish_speed, bomb_speed, bomb_count = get_game_params(difficulty)
    win_score = get_win_score(difficulty)

    player = Player()
    fishes = [Fish(fish_speed) for _ in range(5)]
    bombs = [Bomb(fishes, bomb_speed) for _ in range(bomb_count)]

    score = 0
    font = pygame.font.Font(None, 72)
    game_over = False
    game_win = False
    secret_code_entered = False
    secret_code = [pygame.K_3, pygame.K_3, pygame.K_0, pygame.K_1]
    secret_code_input = []

    game_paused = False

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
            if event.type == pygame.WINDOWFOCUSLOST:
                game_paused = True
            if event.type == pygame.WINDOWFOCUSGAINED:
                game_paused = False

        if game_paused:
            screen.fill(BLACK)
            pause_text = font.render("ПАУЗА", True, WHITE)
            pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(pause_text, pause_rect)
            pygame.display.flip()
            continue

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

        score_text = font.render(f"Счет: {score}/{win_score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()

        if score >= win_score:
            game_win = True

        if game_over or game_win:
            conn = create_connection()
            create_user(conn, user_name, score, difficulty)

            screen.fill(BLACK)
            if game_over:
                game_over_text = font.render("ВЫ ПРОИГРАЛИ!", True, RED)
                text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                score_text_over = font.render(f"Ваш счёт: {score} плаке плаке", True, WHITE)
                text_rect_score = score_text_over.get_rect(center=(WIDTH // 2, HEIGHT // 1.7))
                screen.blit(game_over_text, text_rect)
                screen.blit(score_text_over, text_rect_score)
            elif game_win:
                win_text = font.render("ВЫ ПОБЕДИЛИ!", True, GREEN)
                text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                score_text_win = font.render(f"Ваш счёт: {score} тигр лев брат", True, WHITE)
                text_rect_win = score_text_win.get_rect(center=(WIDTH // 2, HEIGHT // 1.7))
                screen.blit(win_text, text_rect)
                screen.blit(score_text_win, text_rect_win)

            results = get_users_by_difficulty(conn, difficulty)
            display_results(screen, results, difficulty, 0)
            conn.close()
            pygame.display.flip()
            pygame.time.delay(5000)
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