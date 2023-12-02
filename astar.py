import heapq
from GeradorGrafo import GeradorGrafo
from FunctionObjetivo import Objetivo
import numpy as np


class Astar:
    def __init__(self, board):
        self.G = GeradorGrafo(board=board)
        self.root = self.G.root
        self.bestSolution = self.G.bestSolution
        self.worstSolution = self.G.worstSolution
        self.strategy_decision = Objetivo.strategy_decision

    def heuristic(self,node, strategy):
        # Heurística: contar o número de sequências vitoriosas para o jogador atual
        player_wins = 1/node.stepsPlayer if node.stepsPlayer != 0 else float('inf')
        opponent_wins = 1/node.stepsOpponent if node.stepsOpponent != 0 else float('inf')
        return player_wins - opponent_wins #if strategy == 'vence' else opponent_wins - player_wins

    def a_star(self,initial_node, best_solution, worst_solution, strategy):
        print('astar', strategy)
        open_set = [(self.heuristic(initial_node, strategy), initial_node)]
        closed_set = set()
        objetivo = None

        while open_set:
            _, current_node = heapq.heappop(open_set)

            # if current_node.stepsPlayer == best_solution:
            if ((strategy == 'vence' and current_node.stepsPlayer == best_solution) or (strategy == 'impede' and current_node.stepsOpponent == worst_solution)):
                objetivo = current_node
                break
                # return current_node  # Encontrou um estado de vitória

            # closed_set.add(tuple(current_node.board))  # Adiciona o estado atual ao conjunto fechado
            closed_set.add(map(tuple, current_node.board))  # Adiciona o estado atual ao conjunto fechado

            for child in current_node.children:
                # if tuple(child.board.tolist) not in closed_set:
                if map(tuple, child.board) not in closed_set:
                    heapq.heappush(open_set, (self.heuristic(child, strategy), child))

        return self.get_path(objetivo)

        # return None  # Nenhum estado de vitória encontrado

    def astar(self):
        strategy = Objetivo().strategy_decision(self.root)
        caminho = self.a_star(self.root, self.bestSolution, self.worstSolution, strategy)

        origin = np.array(caminho[-2].board)
        moved = np.array(caminho[-1].board)
        posicao_diferenca = np.where(origin != moved)
        if len(posicao_diferenca[0]) > 0:
            pos = tuple(zip(posicao_diferenca[0], posicao_diferenca[1]))
            return pos[0][1]
        else:
            return None

    def get_path(self,node):
        path = []
        while node is not None:
            path.insert(0, node)
            node = node.parent
        return path