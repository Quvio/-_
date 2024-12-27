import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы для размеров игрового поля и клеток
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS  # Размер одной клетки

# Цвета для фигур и фона
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Цвет для выделения выбранной фигуры

# Начальное состояние игрового поля
board = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0]
]

# Создание окна Pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Шашки')  # Заголовок окна

# Шрифт для отображения текста текущего хода
font = pygame.font.SysFont(None, 36)

def draw_board():
    """Функция для отрисовки игрового поля."""
    screen.fill(WHITE)  # Заполнение фона белым цветом
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            # Рисуем черные клетки
            pygame.draw.rect(screen, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(board, selected_piece):
    """Функция для отрисовки фигур на доске."""
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:  # Белая фигура
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                pygame.draw.circle(screen, WHITE,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3-2)
            elif board[row][col] == 2:  # Черная фигура
                pygame.draw.circle(screen, WHITE,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),SQUARE_SIZE // 3)
                pygame.draw.circle(screen, BLACK,(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),SQUARE_SIZE // 3 - 2)
            elif board[row][col] == 3:  # Белая королева
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3-2)
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)
            elif board[row][col] == 4:  # Черная королева
                pygame.draw.circle(screen, BLACK, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)
                pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)

    # Рисуем жёлтую рамку вокруг выбранной фигуры
    if selected_piece is not None:
        row, col = selected_piece
        pygame.draw.rect(screen, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

def draw_turn_text(turn):
    """Функция для отображения текста текущего хода."""
    text = font.render(f"Ход: {'Белых' if turn == 1 else 'Черных'}", True, RED)
    screen.blit(text, (10, 10))  # Отображаем текст в верхнем левом углу

def get_square_from_pos(pos):
    """Функция для получения координат клетки по позиции мыши."""
    x, y = pos
    row = y // SQUARE_SIZE  # Определяем строку
    col = x // SQUARE_SIZE  # Определяем столбец
    return row, col

def is_valid_move(board, start, end):
    """Функция для проверки, является ли ход допустимым."""
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]

    # Определяем изменения по строкам и столбцам
    row_diff = end_row - start_row
    col_diff = end_col - start_col

    # Возвращаем вектор направления
    direction = (row_diff // abs(row_diff) if row_diff != 0 else 0,
                 col_diff // abs(col_diff) if col_diff != 0 else 0)

    # Проверяем, что целевая клетка пуста
    if board[end_row][end_col] != 0:
        return False

    # Проверяем, является ли ход допустимым для обычной фигуры
    if piece == 2:  # Белая фигура
        if end_row < start_row and (end_col == start_col - 1 or end_col == start_col + 1) and abs(end_row - start_row) == 1:
            return True  # Обычный ход
        elif end_row == start_row - 2 and end_col == start_col - 2 and (board[start_row - 1][start_col - 1] == 1 or board[start_row - 1][start_col - 1] == 3):
            return True  # Захват влево
        elif end_row == start_row - 2 and end_col == start_col + 2 and (board[start_row - 1][start_col + 1] == 1 or board[start_row - 1][start_col + 1] == 3):
            return True  # Захват вправо
    elif piece == 1:  # Черная фигура
        if end_row > start_row and (end_col == start_col - 1 or end_col == start_col + 1) and abs(end_row - start_row) == 1:
            return True  # Обычный ход
        elif end_row == start_row + 2 and end_col == start_col - 2 and (board[start_row + 1][start_col - 1] == 2 or board[start_row + 1][start_col - 1] == 4):
            return True  # Захват влево
        elif end_row == start_row + 2 and end_col == start_col + 2 and (board[start_row + 1][start_col + 1] == 2 or board[start_row + 1][start_col + 1] == 4):
            return True  # Захват вправо
    elif piece == 3 or piece == 4:  # Проверка для королев
        count = 0

        for i in range(1, abs(row_diff)):
            new_row = start_row + i * direction[0]
            new_col = start_col + i * direction[1]
            if board[new_row][new_col] != 0:
                count += 1  # Считаем количество захваченных фигур
            if turn == 1 and (board[new_row][new_col] == 1 or board[new_row][new_col] == 3):
                return False  # Запрещаем захват своих фигур
            elif turn == 2 and (board[new_row][new_col] == 2 or board[new_row][new_col] == 4):
                return False  # Запрещаем захват своих фигур
        if count >= 2:
            return False  # Запрещаем захват более одной фигуры
        elif abs(start_col - end_col) == abs(start_row - end_row):
            return True  # Ход допустим

    return False  # Если ни одно из условий не выполнено, ход недопустим

def make_move(board, start, end):
    """Функция для выполнения хода."""
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]

    board[start_row][start_col] = 0  # Убираем фигуру с начальной позиции
    board[end_row][end_col] = piece  # Устанавливаем фигуру на конечную позицию

    if abs(end_row - start_row) >= 2:  # Проверяем, был ли захват
        if piece == 1 or piece == 2:
            # Проверяем, является ли ход захватом
            captured_row = (start_row + end_row) // 2
            captured_col = (start_col + end_col) // 2
            board[captured_row][captured_col] = 0  # Убираем захваченную фигуру

        if piece == 3 or piece == 4:  # Если это королева
            # Определяем изменения по строкам и столбцам
            row_diff = end_row - start_row
            col_diff = end_col - start_col

            # Возвращаем вектор направления
            direction = (row_diff // abs(row_diff) if row_diff != 0 else 0,
                         col_diff // abs(col_diff) if col_diff != 0 else 0)

            for i in range(abs(row_diff)):
                new_row = start_row + i * direction[0]
                new_col = start_col + i * direction[1]
                if board[new_row][new_col] != 0:
                    board[new_row][new_col] = 0  # Убираем все захваченные фигуры

    # Проверяем, достигла ли фигура последнего ряда и превращаем её в королеву
    if end_row == 0 and piece == 2:  # Белая фигура достигает последнего ряда
        board[end_row][end_col] = 4  # 4 обозначает Белую королеву
    if end_row == 7 and piece == 1:  # Черная фигура достигает последнего ряда
        board[end_row][end_col] = 3  # 3 обозначает Черная королеву
    pygame.display.update()  # Обновляем экран

def check_winner(board):
    """Функция для проверки победителя."""
    red_pieces = sum(1 for row in board for piece in row if piece == 1 or piece == 3)
    blue_pieces = sum(1 for row in board for piece in row if piece == 2 or piece == 4)

    if red_pieces == 0:
        return "Белые выиграли!"
    elif blue_pieces == 0:
        return "Черные выиграли!"
    return None

def display_winner(winner_text):
    """Функция для отображения окна победы."""
    screen.fill(WHITE)  # Заполняем фон белым цветом
    text = font.render(winner_text, True, BLACK)  # Создаем текст победителя
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Центрируем текст
    screen.blit(text, text_rect)  # Отображаем текст
    pygame.display.update()  # Обновляем экран
    pygame.time.wait(3000)  # Ждем 3 секунды перед выходом
    pygame.quit()
    sys.exit()

selected_piece = None  # Переменная для хранения выбранной фигуры
turn = 1  # 1 для Белых, 2 для Чернаях

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на выход из игры
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Проверка на нажатие кнопки мыши
            pos = pygame.mouse.get_pos()  # Получаем позицию мыши
            row, col = get_square_from_pos(pos)  # Получаем координаты клетки
            if selected_piece is None:  # Если фигура не выбрана
                if board[row][col] == turn or board[row][col] == turn + 2:  # Проверяем, принадлежит ли фигура текущему игроку
                    selected_piece = (row, col)  # Выбираем фигуру
            else:
                if selected_piece == (row, col):  # Если фигура выбрана снова, снимаем выбор
                    selected_piece = None
                elif is_valid_move(board, selected_piece, (row, col)):  # Проверяем, допустим ли ход
                    make_move(board, selected_piece, (row, col))  # Выполняем ход
                    selected_piece = None  # Снимаем выбор фигуры
                    turn = 3 - turn  # Смена хода

    draw_board()  # Отрисовка игрового поля
    draw_pieces(board, selected_piece)  # Отрисовка фигур
    draw_turn_text(turn)  # Отрисовка текста текущего хода

    winner = check_winner(board)  # Проверяем, есть ли победитель
    if winner:
        display_winner(winner)  # Отображаем окно победы

    pygame.display.update()  # Обновление экрана
