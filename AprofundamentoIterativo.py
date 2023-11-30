from Grafo import Node
from copy import deepcopy
from collections import deque
import numpy as np
from FunctionObjetivo import Objetivo
import json
from Encripita import decodificar, codificar
from astar import a_star


PROFUNDIDADE = 5


class AprofundamentoIterativo:

    def __init__(self, board) -> None:
        self.__board = board
        self.__player = ''
        self.__adversario = ''
        self.bestSolution = float('inf')
        self.worstSolution = float('inf')
        self.playerAtual()
        self.root = self.setaNodo(Node(board), PROFUNDIDADE+1, False)
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

    def setaNodo(self, nodo, profundidade, debug=False):

        nodo.proxPlayer = (self.__adversario if profundidade % 2 else self.__player) if PROFUNDIDADE % 2 else (
            self.__adversario if profundidade % 2 == 0 else self.__player)
        nodo.stepsPlayer = Objetivo().steps_to_win(nodo.board, self.__player, debug) * 2
        nodo.stepsPlayer -= (1 if nodo.proxPlayer == self.__player else 0) #if nodo.stepsPlayer else 0
        self.bestSolution = min(self.bestSolution, nodo.stepsPlayer)
        nodo.stepsOpponent = Objetivo().steps_to_win( nodo.board, self.__adversario, debug) * 2
        nodo.stepsOpponent -= (1 if nodo.proxPlayer == self.__adversario else 0) #if nodo.stepsOpponent else 0
        self.worstSolution = min(self.worstSolution, nodo.stepsOpponent)
        return nodo


    def geraGrafo(self, root, profundidade=PROFUNDIDADE, file_counter=1):
        if profundidade == 0:
            return

        for n in range(7):
            aux = Node(np.copy(root.board), root)
            # board = [row[:] for row in root.board]
            # aux = Node(board)
            for i in range(5, -1, -1):
                if aux.board[i][n] == ' ':
                    aux.board[i][n] = (
                        self.__adversario if profundidade % 2 else self.__player
                    ) if PROFUNDIDADE % 2 == 0 else (
                        self.__adversario if profundidade % 2 == 0 else self.__player
                    )

                    self.setaNodo(aux, profundidade)

                    if aux.stepsPlayer != 0 and aux.stepsOpponent != 0:
                        self.geraGrafo(aux, profundidade - 1, file_counter)

                    root.add_child(aux)

                    break

    def busca(self):
        """
        Realiza a busca na arvore de possibilidades e retorna baseado na estratégia
        """

        strategy = self.strategy_decision(self.root)
        caminho = self.IDDFS(self.root, strategy, self.__player, PROFUNDIDADE+1)
        # for node in caminho:
        #     node.print_node()

        if caminho is not None:
            if strategy == 'vence':
                origin = np.array(caminho[0].board)
                moved = np.array(caminho[1].board)
            else:
                origin = np.array(caminho[-2].board)
                moved = np.array(caminho[-1].board)
            posicao_diferenca = np.where(origin != moved)
            if len(posicao_diferenca[0]) > 0:
                pos = tuple(zip(posicao_diferenca[0], posicao_diferenca[1]))
                return pos[0][1]
            else:
                return None
            
    def astar(self):
        strategy = self.strategy_decision(self.root)
        caminho = a_star(self.root, self.bestSolution, self.worstSolution, strategy)
        # for node in caminho:
        #     node.print_node()

        origin = np.array(caminho[-2].board)
        moved = np.array(caminho[-1].board)
        posicao_diferenca = np.where(origin != moved)
        if len(posicao_diferenca[0]) > 0:
            pos = tuple(zip(posicao_diferenca[0], posicao_diferenca[1]))
            return pos[0][1]
        else:
            return None

    def strategy_decision(self, node):
        my_steps_to_win = node.stepsPlayer
        opponent_steps_to_win = node.stepsOpponent

        if my_steps_to_win == 0:
            return 'vence'  # Já estou prestes a vencer
        elif opponent_steps_to_win == 0:
            return 'impede'  # Adversário está prestes a vencer, preciso impedir
        elif my_steps_to_win <= opponent_steps_to_win or opponent_steps_to_win > 4:
            return 'vence'  # Estou mais próximo da vitória
        else:
            return 'impede'  # Adversário está mais próximo da vitória, preciso impedir

    def IDDFS(self, root, strategy, _goal, max_depth):
        print('it', strategy)
        for depth in range(max_depth):
            path = []
            result = self.DLS(root, goal=_goal, depth=depth,
                              path=path, strategy=strategy)
            if result is not None:
                return result
        return None

    def DLS(self, node, goal, depth, path, strategy):
        path.append(node)
        if ((strategy == 'vence' and node.stepsPlayer == self.bestSolution) or (strategy == 'impede' and node.stepsOpponent == self.worstSolution)):
            return path
        elif depth > 0:
            for child in node.children:
                result = self.DLS(child, goal, depth - 1, path, strategy)
                if result is not None:
                    return result
                path.pop()
        return None


# example_board = [
#     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', ' ', ' ', ' ', ' ', ' ', ' '],
#     [' ', 'X', ' ', ' ', ' ', 'X', ' '],
#     [' ', 'O', 'X', 'O', 'X', 'X', ' '],
#     ['X', 'O', 'O', 'X', 'O', 'O', 'O'],
# ]


# problem = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
# [' ', ' ', 'X', ' ', ' ', ' ', ' '],
# [' ', ' ', 'O', ' ', ' ', ' ', ' '],
# [' ', ' ', 'O', 'X', ' ', ' ', ' '],
# [' ', ' ', 'O', 'X', ' ', ' ', ' '],
# ['O', 'O', 'X', 'X', 'X', 'O', 'X']
# ]

# ap = AprofundamentoIterativo(problem).busca()
