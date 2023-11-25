class Node:
    def __init__(self, name):
        self.children = []
        self.name = name

    def add_child(self, node):
        self.children.append(node)


def print_tree(node, level=0, count = 0):
    print('  ' * level + f'{count}')
    for child in node.children:
        print_tree(child, level + 1, count + 1)


# Criação da árvore
root = Node('A')
b = Node('B')
c = Node('C')
d = Node('D')
e = Node('E')
f = Node('F')

root.add_child(b)
root.add_child(c)
b.add_child(d)
b.add_child(e)
c.add_child(f)

# Impressão da árvore
print_tree(root)
