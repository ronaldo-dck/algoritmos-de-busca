class Node:
    def __init__(self, board, victory = ' '):
        self.children = []
        self.board = board
        self.victory = victory

    def add_child(self, node):
        self.children.append(node)