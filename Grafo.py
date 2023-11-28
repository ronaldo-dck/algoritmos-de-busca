class Node:
    def __init__(self, board):
        self.children = []
        self.board = board
        self.player = ' '
        self.stepsPlayer = float('inf')
        self.stepsOpponent = float('inf')

    def add_child(self, node):
        self.children.append(node)

    def print_node(self):
        print("Board:")
        for row in self.board:
            print(row)
        print(f"Player: {self.player}")
        print(f"Steps to Player's Victory: {self.stepsPlayer}")
        print(f"Steps to Opponent's Victory: {self.stepsOpponent}")
        print("Children:")
        print("----")
        input()