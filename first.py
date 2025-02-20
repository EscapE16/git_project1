import pygame
import random
import sys
import sqlite3
from contextlib import closing

pygame.init()

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    BLACK,
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (0, 255, 255)
]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()


def draw_grid():
    # сеткa игрового поля
    for i in range(SCREEN_WIDTH // BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, SCREEN_HEIGHT))
    for j in range(SCREEN_HEIGHT // BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, j * BLOCK_SIZE), (SCREEN_WIDTH, j * BLOCK_SIZE))


def draw_block(x, y, color):
    # Рисует фигуру на игровом поле
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE + 1, y * BLOCK_SIZE + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2))


def draw_figure(figure, offset_x, offset_y, color):
    # Рисует фигуры
    for y, row in enumerate(figure):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x + offset_x, y + offset_y, color)


def create_figure():
    # Создание фигуры
    shape = random.choice(SHAPES)
    color = random.randint(1, len(COLORS) - 1)
    return {'shape': shape, 'color': color, 'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 'y': 0}


def check_collision(figure, grid, offset_x, offset_y):
    # Проверка на столкновение блоков
    for y, row in enumerate(figure['shape']):
        for x, cell in enumerate(row):
            if cell:
                new_x = figure['x'] + x + offset_x
                new_y = figure['y'] + y + offset_y
                if new_x < 0 or new_x >= SCREEN_WIDTH // BLOCK_SIZE or new_y >= SCREEN_HEIGHT // BLOCK_SIZE:
                    return True
                if new_y >= 0 and grid[new_y][new_x]:
                    return True
    return False


def merge_figure(figure, grid):
    for y, row in enumerate(figure['shape']):
        for x, cell in enumerate(row):
            if cell:
                grid[figure['y'] + y][figure['x'] + x] = figure['color']


def remove_completed_lines(grid):
    # Удаление строки
    lines_removed = 0
    for y, row in enumerate(grid):
        if all(row):
            del grid[y]
            grid.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            lines_removed += 1
    return lines_removed


def draw_score(score):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text_surface, (10, 10))


def draw_text(text, size, color, y_offset=0):
    # Создает текстовую поверхность
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_offset))
    return text_surface, text_rect


def get_db_connection():
    conn = sqlite3.connect('records.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS records
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     score INTEGER NOT NULL,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    return conn


def save_record(name, score):
    with closing(get_db_connection()) as conn:
        conn.execute('INSERT INTO records (name, score) VALUES (?, ?)', (name, score))
        conn.commit()


def get_top_records(limit=10):
    with closing(get_db_connection()) as conn:
        cursor = conn.execute('SELECT name, score FROM records ORDER BY score DESC LIMIT ?', (limit,))
        return cursor.fetchall()


def input_name(score):
    name = ""
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)

        title = font.render("NEW HIGH SCORE!", True, (255, 215, 0))
        prompt = font.render("Enter your name:", True, WHITE)
        input_text = font.render(name + "|", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)

        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 250))
        screen.blit(input_text, (SCREEN_WIDTH // 2 - input_text.get_width() // 2, 300))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15 and event.unicode.isalnum():
                        name += event.unicode


def show_records_screen():
    records = get_top_records()
    font = pygame.font.Font(None, 36)

    while True:
        screen.fill(BLACK)

        title = font.render("TOP SCORES", True, (255, 215, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        y = 150
        for i, (name, score) in enumerate(records, 1):
            text = font.render(f"{i}. {name} - {score}", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y))
            y += 40

        back_text = font.render("Press ESC to return", True, WHITE)
        screen.blit(back_text, (SCREEN_WIDTH // 2 - back_text.get_width() // 2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return


def draw_button(text, rect, active_color, inactive_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse_pos):
        color = active_color
        if click[0] == 1 and action is not None:
            action()
    else:
        color = inactive_color

    pygame.draw.rect(screen, color, rect)

    font = pygame.font.Font(None, 36)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)


def menu_screen():
    while True:
        screen.fill(BLACK)

        title, title_rect = draw_text("TETRIS", 72, WHITE, y_offset=-100)
        screen.blit(title, title_rect)

        button_width = 200
        button_height = 50
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 300, button_width, button_height)
        quit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 370, button_width, button_height)
        records_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, 440, button_width, button_height)

        draw_button("Start Game", start_button, (50, 200, 50), (0, 100, 0), lambda: start_game())
        draw_button("Exit", quit_button, (200, 50, 50), (100, 0, 0), lambda: quit_game())
        draw_button("High Scores", records_button, (100, 100, 200), (50, 50, 150), lambda: show_records_screen())

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def start_game():
    main()
    menu_screen()


def quit_game():
    pygame.quit()
    sys.exit()


def main():
    grid = [[0 for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    figure = create_figure()
    score = 0
    game_over = False
    fall_time = 0
    fall_speed = 500

    while not game_over:
        screen.fill(BLACK)
        draw_grid()
        current_time = pygame.time.get_ticks()

        # Управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(figure, grid, -1, 0):
                    figure['x'] -= 1
                if event.key == pygame.K_RIGHT and not check_collision(figure, grid, 1, 0):
                    figure['x'] += 1
                if event.key == pygame.K_DOWN:
                    if not check_collision(figure, grid, 0, 1):
                        figure['y'] += 1
                        score += 1
                if event.key == pygame.K_UP:
                    rotated_figure = list(zip(*reversed(figure['shape'])))
                    if not check_collision({'shape': rotated_figure, 'x': figure['x'], 'y': figure['y']}, grid, 0, 0):
                        figure['shape'] = rotated_figure

        if current_time - fall_time > fall_speed:
            if not check_collision(figure, grid, 0, 1):
                figure['y'] += 1
                fall_time = current_time
            else:
                merge_figure(figure, grid)
                lines_removed = remove_completed_lines(grid)
                score += lines_removed * 100
                figure = create_figure()
                if check_collision(figure, grid, 0, 0):
                    game_over = True

        draw_figure(figure['shape'], figure['x'], figure['y'], COLORS[figure['color']])
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell:
                    draw_block(x, y, COLORS[cell])
        draw_score(score)
        pygame.display.flip()
        clock.tick(30)

    records = get_top_records()
    if len(records) < 10 or score > records[-1][1]:
        name = input_name(score)
        if name.strip():
            save_record(name.strip(), score)

    show_records_screen()


if __name__ == "__main__":
    menu_screen()