from Grafo import Node
import numpy as np
from FunctionObjetivo import Objetivo
import hp

PROFUNDIDADE = hp.PROFUNDIDADE

class GeradorGrafo:

    def __init__(self, board):
        self.__board = board
        self.__player = ''
        self.__adversario = ''
        self.bestSolution = float('inf')
        self.worstSolution = float('inf')
        self.playerAtual()
        self.root = self.setaNodo(Node(board), PROFUNDIDADE+1, False)
        self.geraGrafo(self.root, PROFUNDIDADE)

    def getPlayer(self):
        return self.__player

    def playerAtual(self):
        contagem_nao_vazios = sum(
            1 for linha in self.__board for elemento in linha if elemento != ' ')
        self.__player = 'X' if contagem_nao_vazios % 2 == 0 else 'O'
        self.__adversario = 'O' if self.__player == 'X' else 'X'

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
