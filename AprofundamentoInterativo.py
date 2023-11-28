from Grafo import Node
from copy import deepcopy
from collections import deque
import numpy as np

PROFUNDIDADE = 6
class AprofundamentoIterativo:

    def __init__(self, board) -> None:
        self.__board = board
        self.__player = ''
        self.__adversario = ''
        self.playerAtual()
        self.root = self.setaNodo(Node(board), PROFUNDIDADE, True)
        self.geraGrafo(self.root, PROFUNDIDADE)

    def playerAtual(self):
        contagem_nao_vazios = sum(
            1 for linha in self.__board for elemento in linha if elemento != ' ')
        self.__player = 'X' if contagem_nao_vazios % 2 == 0 else 'O'
        self.__adversario = 'O' if self.__player == 'X' else 'X'

    @staticmethod
    def print_board(board):
        for row in board:
            for row in board:
                print(row)
            print("_" * 54)

    def steps_to_win(self, board, goal, debug = False):
        
        # Check horizontal
        for row in board:
            if f'{goal}{goal}{goal}{goal}' in ''.join(row):
                return 0 #+ minhaVez  # Já venceu na horizontal

        # Check vertical
        for col in range(7):
            column = ''.join(board[row][col] for row in range(6))
            if f'{goal}{goal}{goal}{goal}' in column:
                return 0 #+ minhaVez  # Já venceu na vertical

        # Check diagonals
        for i in range(3):
            for j in range(4):
                if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == goal:
                    return 0 #+ minhaVez  # Já venceu na diagonal

        for i in range(3):
            for j in range(3, 7):
                if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == goal:
                    return 0 #+ minhaVez  # Já venceu na diagonal

        # Calcular a menor distância até a vitória
        min_distance = float('inf')

        # Check horizontal
        for i,row in enumerate(board):
            for groups in range(0,4): 
                goal_count = 0
                empty_count = 0
                for n in range(0,4):
                    if row[groups + n] == goal:
                        goal_count += 1
                    elif row[groups + n] != ' ':
                        goal_count = 0
                        empty_count = float('inf')
                        break
                    column = ''.join(board[linha][groups + n] for linha in range(i+1, 6))
                    for cell in column:
                        if cell == ' ':
                            empty_count +=1
                min_distance = min(min_distance, 4 - goal_count + empty_count)
            # if debug: print('linha ', min_distance)

        # Check vertical
        for col in range(7):
            column = ''.join(board[row][col] for row in range(6))
            for groups in range(0, 3):
                goal_count = 0
                for n in range(0,4):
                    if column[groups + n] == goal:
                        goal_count += 1
                    elif column[groups + n] != ' ':
                        goal_count = 0
                        break
                    
                min_distance = min(min_distance, 4 - goal_count)
            # if debug: print('coluna ', min_distance)

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
                    column = ''.join(board[linha][j + k] for linha in range(i+k+1, 6))
                    for cell in column:
                        if cell == ' ':
                            empty_count +=1

                
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
                    column = ''.join(board[linha][j - k] for linha in range(i+k+1, 6))
                    for cell in column:
                        if cell == ' ':
                            empty_count +=1
                min_distance = min(min_distance, 4 - consecutive_count)
                # if debug: print('diagonal 2', min_distance)

        return min_distance
        
    def setaNodo(self, nodo, profundidade, debug = False):
        nodo.stepsPlayer = self.steps_to_win(nodo.board, self.__player, debug)
        nodo.stepsOpponent = self.steps_to_win(nodo.board, self.__adversario, debug)
        nodo.player = (self.__adversario if profundidade % 2 else self.__player) if PROFUNDIDADE % 2 == 0 else (self.__adversario if profundidade % 2 == 0 else self.__player)
        return nodo

    def geraGrafo(self, root, profundidade=PROFUNDIDADE):

        if profundidade == 0:
            return

        for n in range(7):
            aux = Node(deepcopy(root.board))
            for i in range(5, -1, -1):
                if aux.board[i][n] == ' ':

                    aux.board[i][n] = (self.__adversario if profundidade % 2 else self.__player) if PROFUNDIDADE % 2 == 0 else (self.__adversario if profundidade % 2 == 0 else self.__player)

                    self.setaNodo(aux, profundidade)

                    if aux.stepsPlayer > 0 or aux.stepsOpponent > 0:
                        self.geraGrafo(aux, profundidade - 1)

                    root.add_child(aux)
                    break

    def busca(self):
        strategy = self.strategy_decision(self.root)
        print(strategy)
        self.root.print_node()
        caminho = self.IDDFS(self.root, self.__player, PROFUNDIDADE+1)
        print(np.array(caminho))

        if caminho is not None:
            if strategy == 'vence':
                origin = np.array(caminho[0])
                moved = np.array(caminho[1])
            else:
                origin = np.array(caminho[-2])
                moved = np.array(caminho[-1])
            posicao_diferenca = np.where(origin != moved)
            if len(posicao_diferenca[0]) > 0:
                pos = tuple(zip(posicao_diferenca[0], posicao_diferenca[1]))
                print(pos) # o bug aqui acontecia pq não tinha como garantir q a ordem das alterações fosse detectada tal qual elas aconteceram cronologicamente, então podia ser que o movimento da vitória do oponente não estivesse na última posição. Agr tá garantido que entre origin e moved existe apenas uma jogada de diferença, portanto essa variação do index do pos abaixo não é mais relevante
                # if strategy == 'vence':
                #     return pos[0][1]
                # return pos[-1][1]
                return pos[0][1]
            else:
                return None


    def DLS(self, node, goal, depth, path, strategy):
        path.append(node.board)
        if ((strategy == 'vence' and node.stepsPlayer == 0) or (strategy == 'impede' and node.stepsOpponent == 0)):
            return path
        elif depth > 0:
            for child in node.children:
                result = self.DLS(child, goal, depth - 1, path, strategy)
                if result is not None:
                    return result
                path.pop()
        return None

    def strategy_decision(self, node):
        my_steps_to_win = node.stepsPlayer
        opponent_steps_to_win = node.stepsOpponent

        # node.print_node()
        if my_steps_to_win == 0:
            return 'vence'  # Já estou prestes a vencer
        elif opponent_steps_to_win == 0:
            return 'impede'  # Adversá rio está prestes a vencer, preciso impedir
        elif my_steps_to_win <= opponent_steps_to_win:
            return 'vence'  # Estou mais próximo da vitória
        else:
            return 'impede'  # Adversário está mais próximo da vitória, preciso impedir

    def IDDFS(self, root, _goal, max_depth):
        for depth in range(max_depth):
            path = []
            # Substitua 'X' pelo seu objetivo
            strategy = self.strategy_decision(root)
            print('estrategia', strategy)
            result = self.DLS(root, goal=_goal, depth=depth, path=path, strategy=strategy)
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


example_board = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', 'O', ' ', ' ', ' ', ' '],
    [' ', ' ', 'O', ' ', ' ', ' ', ' '],
    [' ', ' ', 'O', ' ', ' ', ' ', ' '],
    [' ', ' ', 'X', 'X', ' ', ' ', ' '],
]

# problem = [[' ' ' ' ' ' ' ' ' ' ' ' ' ']
            # [' ' ' ' 'X' ' ' ' ' ' ' ' ']
            # [' ' ' ' 'O' ' ' ' ' ' ' ' ']
            # [' ' ' ' 'O' 'X' ' ' ' ' ' ']
            # [' ' ' ' 'O' 'X' ' ' ' ' ' ']
            # ['O' 'O' 'X' 'X' 'X' 'O' 'X']


# ap = AprofundamentoIterativo(example_board)
