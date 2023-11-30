import heapq
from Grafo import Node

def heuristic(node, strategy):
    # Heurística: contar o número de sequências vitoriosas para o jogador atual
    player_wins = 1/node.stepsPlayer if node.stepsPlayer != 0 else float('inf')
    opponent_wins = 1/node.stepsOpponent if node.stepsOpponent != 0 else float('inf')
    return player_wins - opponent_wins #if strategy == 'vence' else opponent_wins - player_wins

def a_star(initial_node, best_solution, worst_solution, strategy):
    print('astar', strategy)
    open_set = [(heuristic(initial_node, strategy), initial_node)]
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
                heapq.heappush(open_set, (heuristic(child, strategy), child))

    return get_path(objetivo)

    # return None  # Nenhum estado de vitória encontrado



def get_path(node):
    path = []
    while node is not None:
        path.insert(0, node)
        node = node.parent
    return path