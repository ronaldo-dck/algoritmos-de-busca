import numpy as np
from FunctionObjetivo import Objetivo
from GeradorGrafo import GeradorGrafo
import time
import hp

PROFUNDIDADE = hp.PROFUNDIDADE


class AprofundamentoIterativo:
    def __init__(self, board):
        self.G = GeradorGrafo(board=board)
        self.root = self.G.root
        self.bestSolution = self.G.bestSolution
        self.worstSolution = self.G.worstSolution
        self.AccessCount = 0

    def busca(self):
        """
        Realiza a busca na arvore de possibilidades por meio de aprofundamento interativo e retorna baseado na estratégia
        """
        time_inicio = time.time()

        strategy = Objetivo().strategy_decision(self.root)
        caminho = self.IDDFS(self.root, strategy,
                             self.G.getPlayer(), PROFUNDIDADE+1)
        print('IT Acessos: ', self.AccessCount)

        # for node in caminho:
        #     node.print_node()

        if caminho is not None:
            if strategy == 'vence':
                origin = np.array(caminho[-2].board)
                moved = np.array(caminho[-1].board)
            else:
                origin = np.array(caminho[-2].board)
                moved = np.array(caminho[-1].board)
            posicao_diferenca = np.where(origin != moved)
            if len(posicao_diferenca[0]) > 0:
                pos = tuple(zip(posicao_diferenca[0], posicao_diferenca[1]))
                time_fim = time.time()
                print("busca iterativa ",time_fim-time_inicio)
                return pos[0][1]
            else:
                return None

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
                self.AccessCount += 1
                result = self.DLS(child, goal, depth - 1, path, strategy)
                if result is not None:
                    return result
                path.pop()
        return None
