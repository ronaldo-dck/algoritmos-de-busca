import math


class ConnectFourAI:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def evaluate_board(self, board, player):
        # Função de avaliação simples para o Connect Four
        score = 0
        opponent = 'O' if player == 'X' else 'X'

        for row in board:
            for i in range(4):
                window = row[i:i+4]
                score += self.evaluate_window(window, player, opponent)

        for col in range(7):
            for i in range(3):
                window = [board[i+k][col] for k in range(4)]
                score += self.evaluate_window(window, player, opponent)

        for i in range(3):
            for j in range(4):
                window = [board[i+k][j+k] for k in range(4)]
                score += self.evaluate_window(window, player, opponent)

                window = [board[i+k][j+3-k] for k in range(4)]
                score += self.evaluate_window(window, player, opponent)

        return score

    def evaluate_window(self, window, player, opponent):
        score = 0
        if window.count(player) == 4:
            score += 100
        elif window.count(player) == 3 and window.count(' ') == 1:
            score += 5
        elif window.count(player) == 2 and window.count(' ') == 2:
            score += 2

        if window.count(opponent) == 3 and window.count(' ') == 1:
            score -= 4

        return score

    def is_terminal_node(self, board):
        return self.check_winner(board, 'X') or self.check_winner(board, 'O') or not any(' ' in row for row in board)

    def check_winner(self, board, player):
        for row in board:
            if ''.join(row).count(player * 4) > 0:
                return True

        for col in range(7):
            column = ''.join([board[row][col] for row in range(6)])
            if column.count(player * 4) > 0:
                return True

        for i in range(3):
            for j in range(4):
                if ''.join([board[i+k][j+k] for k in range(4)]).count(player * 4) > 0:
                    return True

                if ''.join([board[i+k][j+3-k] for k in range(4)]).count(player * 4) > 0:
                    return True

        return False

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        valid_moves = [col for col in range(7) if any(
            row[col] == ' ' for row in board)]

        if depth == 0 or self.is_terminal_node(board):
            return None, self.evaluate_board(board, 'X')

        if maximizing_player:
            max_eval = -math.inf
            best_move = None

            for col in valid_moves:
                row = self.get_next_open_row(board, col)
                temp_board = [row[:] for row in board]
                temp_board[row][col] = 'X'

                _, eval_score = self.minimax(
                    temp_board, depth - 1, False, alpha, beta)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = col

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            return best_move, max_eval
        else:
            min_eval = math.inf
            best_move = None

            for col in valid_moves:
                row = self.get_next_open_row(board, col)
                temp_board = [row[:] for row in board]
                temp_board[row][col] = 'O'

                _, eval_score = self.minimax(
                    temp_board, depth - 1, True, alpha, beta)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = col

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            return best_move, min_eval

    def get_next_open_row(self, board, col):
        for r in range(5, -1, -1):
            if board[r][col] == ' ':
                return r
        return None

    def get_best_move(self, board):
        best_move, _ = self.minimax(
            board, self.max_depth, True, -math.inf, math.inf)
        return best_move


def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 29)


if __name__ == "__main__":
    game_board = [[' ' for _ in range(7)] for _ in range(6)]
    ai = ConnectFourAI(max_depth=3)

    while True:
        print_board(game_board)

        try:
            player_move = int(input("Enter your move (1-7): ")) - 1
            if 0 <= player_move <= 6 and any(row[player_move] == ' ' for row in game_board):
                player_row = ai.get_next_open_row(game_board, player_move)
                game_board[player_row][player_move] = 'X'
            else:
                print("Invalid move. Please try again.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if ai.check_winner(game_board, 'X'):
            print_board(game_board)
            print("You win!")
            break

        if all(all(cell != ' ' for cell in row) for row in game_board):
            print_board(game_board)
            print("It's a draw!")
            break

        print("AI is thinking...")
        ai_move = ai.get_best_move(game_board)
        ai_row = ai.get_next_open_row(game_board, ai_move)
        game_board[ai_row][ai_move] = 'O'

        if ai.check_winner(game_board, 'O'):
            print_board(game_board)
            print("AI wins!")
            break

        if all(all(cell != ' ' for cell in row) for row in game_board):
            print_board(game_board)
            print("It's a draw!")
            break
