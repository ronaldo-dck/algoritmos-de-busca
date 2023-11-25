from Grafo import Node 
from copy import deepcopy
from collections import deque
import numpy as np

class AprofundamentoIterativo:
    
    def __init__(self, board) -> None:
        self.__board = board
        self.root = Node(board)
        self.__player = ''
        self.__adversario = ''
        self.playerAtual()
        self.geraGrafo(self.root)
        self.busca()


    def playerAtual(self):
        contagem_nao_vazios = sum(1 for linha in self.__board for elemento in linha if elemento != ' ')
        self.__player = 'X' if contagem_nao_vazios % 2 == 0 else 'O'
        self.__adversario = 'O' if self.__player == 'X' else 'X'
        print(self.__player, self.__adversario)


    @staticmethod
    def print_board(board):
        for row in board:
            print('|  '.join(row))
            print('-' * 29)

    def check_winner(self, board):
        # Check horizontal
        for row in board:
            if 'XXXX' in ''.join(row) or 'OOOO' in ''.join(row):
                return True

        # Check vertical
        for col in range(7):
            column = ''.join(board[row][col] for row in range(6))
            if 'XXXX' in column or 'OOOO' in column:
                return True

        # Check diagonals
        for i in range(3):
            for j in range(4):
                if (board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == 'X' or
                        board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == 'O'):
                    return True

        for i in range(3):
            for j in range(3, 7):
                if (board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == 'X' or
                        board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == 'O'):
                    return True

        return False

    def geraGrafo(self, root, profundidade = 7):
        
        if profundidade == 0:
            return

        for n in range(7):
            aux = Node(deepcopy(root.board))
            for i in range(5, -1, -1):
                if aux.board[i][n] == ' ' :

                    aux.board[i][n] = self.__player if profundidade % 2 else self.__adversario
                    aux.victory = (aux.board[i][n]) if self.check_winner(aux.board) else ' '

                    if aux.victory == ' ':
                        self.geraGrafo(aux, profundidade - 1)

                    root.add_child(aux)
                    break

    def busca(self):
        caminho = self.IDDFS(self.root, self.__player, 8) 

        if caminho is not None:
            origin = np.array(caminho[0])
            moved = np.array(caminho[1])
            posicao_diferenca = np.where(origin != moved)
            if len(posicao_diferenca[0]) > 0:
                pos = tuple(zip(posicao_diferenca[0], posicao_diferenca[1]))
                return pos[0][1]
            else:
                return None


    def DLS(self, node, goal, depth, path):
        path.append(node.board)
        if depth == 0 and node.victory == goal:
            return path
        elif depth > 0:
            for child in node.children:
                result = self.DLS(child, goal, depth-1, path)
                if result is not None:
                    return result
                path.pop()
        return None


    def IDDFS(self, root, goal, max_depth):
        for depth in range(max_depth):
            path = []
            result = self.DLS(root, goal, depth, path)
            if result is not None:
                return result
        return None






example_board = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', 'X', ' ', ' ', ' ', 'X', ' '],
    [' ', 'O', 'X', 'O', 'X', 'X', ' '],
    ['X', 'O', 'O', 'X', 'O', 'O', 'O'],
]


ap = AprofundamentoIterativo(example_board)