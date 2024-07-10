
import pygame
import random

# Инициализация Pygame
pygame.init()

# Задаем размеры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Стрельба по мишеням")

# Загрузка изображений
background = pygame.image.load('img/forest.jpg')
target_img = pygame.image.load('img/rab.png')
crosshair_img = pygame.image.load('img/scope.png')
shot_img = pygame.image.load('img/hole.png')

# Определение начальных параметров
TARGET_SIZE = 100
target_x = random.randint(0, WIDTH - TARGET_SIZE)
target_y = random.randint(0, HEIGHT - TARGET_SIZE)
target_rect = pygame.Rect(target_x, target_y, TARGET_SIZE, TARGET_SIZE)

# Параметры игры
target_display_time = 1000  # В миллисекундах
misses = 0
hits = 0
shots = 0

# Порог промахов
MAX_MISSES = 5

# Время исчезновения мишени
time_to_hide = pygame.time.get_ticks() + target_display_time

# Инициализация Pygame clock
clock = pygame.time.Clock()

# Основной цикл игры
running = True
game_over = False

while running:
    screen.blit(background, (0, 0))

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shots += 1
            mouse_x, mouse_y = event.pos
            if target_rect.collidepoint(mouse_x, mouse_y) and pygame.time.get_ticks() < time_to_hide:
                hits += 1
                target_x = random.randint(0, WIDTH - TARGET_SIZE)
                target_y = random.randint(0, HEIGHT - TARGET_SIZE)
                target_display_time *= 0.98
                TARGET_SIZE = int(TARGET_SIZE * 0.98)
                target_rect = pygame.Rect(target_x, target_y, TARGET_SIZE, TARGET_SIZE)
                time_to_hide = pygame.time.get_ticks() + target_display_time
            else:
                misses += 1
                if misses >= MAX_MISSES:
                    game_over = True

    # Отображение мишени
    if not game_over and pygame.time.get_ticks() < time_to_hide:
        target_img_resized = pygame.transform.scale(target_img, (TARGET_SIZE, TARGET_SIZE))
        screen.blit(target_img_resized, (target_x, target_y))
    elif not game_over:
        target_x = random.randint(0, WIDTH - TARGET_SIZE)
        target_y = random.randint(0, HEIGHT - TARGET_SIZE)
        target_rect = pygame.Rect(target_x, target_y, TARGET_SIZE, TARGET_SIZE)
        time_to_hide = pygame.time.get_ticks() + target_display_time

    # Отображение прицела
    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(crosshair_img, (mouse_x - crosshair_img.get_width() // 2, mouse_y - crosshair_img.get_height() // 2))

    # Отображение счетчиков
    font = pygame.font.SysFont(None, 36)
    shots_text = font.render(f'Выстрелы: {shots}', True, (255, 255, 255))
    hits_text = font.render(f'Попадания: {hits}', True, (255, 255, 255))
    misses_text = font.render(f'Промахи: {misses}', True, (255, 255, 255))
    screen.blit(shots_text, (10, 10))
    screen.blit(hits_text, (10, 50))
    screen.blit(misses_text, (10, 90))

    if game_over:
        font_large = pygame.font.SysFont(None, 72)
        game_over_text = font_large.render('Игра окончена', True, (255, 0, 0))
        screen.blit(game_over_text,
                    (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

        restart_text = font.render('Нажмите R для рестарта или Q для выхода', True, (255, 255, 255))
        screen.blit(restart_text,
                    (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            misses = 0
            hits = 0
            shots = 0
            TARGET_SIZE = 100
            target_display_time = 1000
            time_to_hide = pygame.time.get_ticks() + target_display_time
            game_over = False
        elif keys[pygame.K_q]:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()