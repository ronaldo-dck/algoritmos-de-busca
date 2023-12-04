class Node:
    def __init__(self, board, parent = None):
        self.parent = parent
        self.children = []
        self.board = board
        self.proxPlayer = ' '
        self.stepsPlayer = float('inf')
        self.stepsOpponent = float('inf')

    def __lt__(self, other):
        return self.stepsPlayer < other.stepsPlayer

    def add_child(self, node):
        self.children.append(node)

    def print_node(self):
        print("Board:")
        for row in self.board:
            print(row)
        print(f"ProxJogador: {self.proxPlayer}")
        print(f"Turnos para vitoria do jogador: {self.stepsPlayer}")
        print(f"Turnos para vitoria do oponente: {self.stepsOpponent}")
        print("Children:")
        print("----")
        input()