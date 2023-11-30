# Poucas coisas aqui estão funcionando corretamente, acho q o próximo passo é começar do zero msm
from flask import Flask, render_template, jsonify, request
# from AprofundamentoIterativo import AprofundamentoIterativo
import threading
app = Flask(__name__)

def createBoard():
    return [[' ' for _ in range(7)] for _ in range(6)]

class ConnectFourAPI:
    def __init__(self, board):
        self.board = board
        self.current_player = 'X'

    def print_board(self):
        for row in self.board:
            print(row)
        print("_" * 54)

    def make_move(self, column):
        for i in range(5, -1, -1):
            if self.board[i][column] == ' ':
                self.board[i][column] = self.current_player
                break
        else:
            print("Column is full. Try again.")
            return False

        return True

    def check_winner(self):
        # Check horizontal
        for row in self.board:
            if 'XXXX' in ''.join(row) or 'OOOO' in ''.join(row):
                return True

        # Check vertical
        for col in range(7):
            column = ''.join(self.board[row][col] for row in range(6))
            if 'XXXX' in column or 'OOOO' in column:
                return True

        # Check diagonals
        for i in range(3):
            for j in range(4):
                if (self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] == 'X' or
                        self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] == 'O'):
                    return True

        for i in range(3):
            for j in range(3, 7):
                if (self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == self.board[i + 3][j - 3] == 'X' or
                        self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == self.board[i + 3][j - 3] == 'O'):
                    return True

        return False

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_player_column(self):
        event = threading.Event()
        pass

    def play_game(self):
        while True:
            self.print_board()

            try:

                if self.current_player == 'X':
                    # column = AprofundamentoIterativo(self.board).astar()#int(input(f"Player {self.current_player}, choose a column (1-7): ")) - 1
                    column = self.get_player_column()
                else:
                    pass
                    # column = AprofundamentoIterativo(self.board).busca()
                    # column = AprofundamentoIterativo(self.board).busca()

                if 0 <= column <= 6:
                    if self.make_move(column):
                        if self.check_winner():
                            self.print_board()
                            print(f"Player {self.current_player} wins!")
                            break
                        self.switch_player()
                    else:
                        continue
                else:
                    print("Invalid column. Please choose a number between 1 and 7.")
            except ValueError:
                print("Invalid input. Please enter a number.")


game = ConnectFourAPI(createBoard())
# gameThread = threading.Thread(target=game.play_game)
# gameThread.start()


@app.route('/move', methods=['POST'])
def move():
    id = request.form.get('id')
    # Handle the move here
    parts = id.split('-')
    row = int(parts[0])
    col = int(parts[1])
    game.board[row][col] = 'X'
    
    return jsonify({'result': 'success', 'board': game.board})

@app.route('/')
def home():
    return render_template('index.html', board=game.board)

if __name__ == '__main__':
    # board = createBoard()
    app.run(debug=True)

