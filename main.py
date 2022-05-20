import numpy as np
import pygame
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
ROWS = 3
COLUMNS = 3
MARGIN = 15
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CIRCLE_COLOUR = (255, 0, 0)
CROSS_COLOUR = (0, 0, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

board = np.zeros((ROWS, COLUMNS))


def draw_lines():
    pygame.draw.line(screen, BLACK, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), MARGIN)
    pygame.draw.line(screen, BLACK, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), MARGIN)
    pygame.draw.line(screen, BLACK, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), MARGIN)
    pygame.draw.line(screen, BLACK, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), MARGIN)


def draw_figures():
    for row in range(ROWS):
        for col in range(COLUMNS):

            if board[row][col] == 1:
                pygame.draw.circle(screen, CROSS_COLOUR, (
                    int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS,
                                   CIRCLE_WIDTH)

            elif board[row][col] == 2:
                pygame.draw.line(screen, CIRCLE_COLOUR,
                                 (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

                pygame.draw.line(screen, CIRCLE_COLOUR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 CROSS_WIDTH)


def mark_square(row, col, user):
    board[row][col] = user


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 0:
                return False
    return True


def draw_vertical_winning_line(col, user):
    pos_x = col * SQUARE_SIZE + SQUARE_SIZE // 2

    if user == 1:
        color = CROSS_COLOUR
    elif user == 2:
        color = CIRCLE_COLOUR

    pygame.draw.line(screen, color, (pos_x, 15), (pos_x, HEIGHT - 15), MARGIN)


def draw_horizontal_winning_line(row, user):
    pos_y = row * SQUARE_SIZE + SQUARE_SIZE // 2

    if user == 1:
        color = CROSS_COLOUR
    elif user == 2:
        color = CIRCLE_COLOUR

    pygame.draw.line(screen, color, (15, pos_y), (WIDTH - 15, pos_y), MARGIN)


def draw_asc_diagonal(user):
    if user == 1:
        color = CROSS_COLOUR
    elif user == 2:
        color = CIRCLE_COLOUR

    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), MARGIN)


def draw_desc_diagonal(user):
    if user == 1:
        color = CROSS_COLOUR
    elif user == 2:
        color = CIRCLE_COLOUR

    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), MARGIN)


def check_win(user):
    for col in range(COLUMNS):
        if board[0][col] == user and board[1][col] == user and board[2][col] == user:
            draw_vertical_winning_line(col, user)
            return True

    for row in range(ROWS):
        if board[row][0] == user and board[row][1] == user and board[row][2] == user:
            draw_horizontal_winning_line(row, user)
            return True

    if board[2][0] == user and board[1][1] == user and board[0][2] == user:
        draw_asc_diagonal(user)
        return True

    if board[0][0] == user and board[1][1] == user and board[2][2] == user:
        draw_desc_diagonal(user)
        return True


def restart():
    screen.fill(WHITE)
    draw_lines()
    for row in range(ROWS):
        for col in range(COLUMNS):
            board[row][col] = 0


draw_lines()

player = 1
finished = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not finished:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            clicked_row = int(mouse_y // SQUARE_SIZE)
            clicked_column = int(mouse_x // SQUARE_SIZE)

            if available_square(clicked_row, clicked_column):

                mark_square(clicked_row, clicked_column, player)
                if check_win(player):
                    finished = True

                player = player % 2 + 1
                draw_figures()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    player = 1
                    finished = False

    pygame.display.update()
