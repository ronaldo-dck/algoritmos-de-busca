import numpy as np


class Objetivo:
    def __init__(self) -> None:
        pass

    def steps_to_win(self, board: np.ndarray, goal, debug=False):
        # Check horizontal

        debug = False
        for row in board:
            if f'{goal}{goal}{goal}{goal}' in ''.join(row):
                return 0  # + minhaVez  # Já venceu na horizontal

        # Check vertical
        for col in range(7):
            column = ''.join(board[row][col] for row in range(6))
            if f'{goal}{goal}{goal}{goal}' in column:
                return 0  # + minhaVez  # Já venceu na vertical

        # Check diagonals
        for i in range(3):
            for j in range(4):
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == goal:
                    return 0  # + minhaVez  # Já venceu na diagonal

        for i in range(3):
            for j in range(3, 7):
                if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == goal:
                    return 0  # + minhaVez  # Já venceu na diagonal

        # Calcular a menor distância até a vitória
        min_distance = float('inf')

        # Check horizontal
        for i, row in enumerate(board):
            for groups in range(0, 4):
                goal_count = 0
                empty_count = 0
                for n in range(0, 4):
                    if row[groups + n] == goal:
                        goal_count += 1
                    elif row[groups + n] != ' ':
                        goal_count = 0
                        empty_count = float('inf')
                        break
                    column = ''.join(board[linha][groups + n]
                                     for linha in range(i+1, 6))
                    for cell in column:
                        if cell == ' ':
                            empty_count += 1
                min_distance = min(min_distance, 4 - goal_count + empty_count)
            if debug: print('linha ', min_distance)

        # Check vertical
        for col in range(7):
            column = ''.join(board[row][col] for row in range(6))
            for groups in range(0, 3):
                goal_count = 0
                for n in range(0, 4):
                    if column[groups + n] == goal:
                        goal_count += 1
                    elif column[groups + n] != ' ':
                        goal_count = 0
                        break

                min_distance = min(min_distance, 4 - goal_count)
            if debug: print('coluna ', min_distance, goal)

        # Check diagonals
        for i in range(3):
            for j in range(4):
                consecutive_count = 0
                for k in range(4):
                    if board[i + k][j + k] == goal:
                        consecutive_count += 1
                    elif board[i + k][j + k] != ' ':
                        consecutive_count = 0
                        break
                    column = ''.join(board[linha][j + k]
                                     for linha in range(i+k+1, 6))
                    for cell in column:
                        if cell == ' ':
                            empty_count += 1

                min_distance = min(min_distance, 4 - consecutive_count)
                # if debug: print('diagonal 1', min_distance)

        for i in range(3):
            for j in range(3, 7):
                consecutive_count = 0
                for k in range(4):
                    if board[i + k][j - k] == goal:
                        consecutive_count += 1
                    elif board[i + k][j - k] != ' ':
                        consecutive_count = 0
                        break
                    column = ''.join(board[linha][j - k]
                                     for linha in range(i+k+1, 6))
                    for cell in column:
                        if cell == ' ':
                            empty_count += 1
                min_distance = min(min_distance, 4 - consecutive_count)
                # if debug: print('diagonal 2', min_distance)

        return min_distance


