# Este código cria um grafo e realiza uma Busca de Aprofundamento Iterativo para encontrar um nó objetivo. A função IDDFS realiza a busca iterativa, aumentando a profundidade a cada iteração até a profundidade máxima. A função DLS realiza a busca em profundidade até a profundidade especificada. Se o nó objetivo for encontrado, a busca é interrompida e o nó é retornado. Caso contrário, a busca continua até que todos os nós tenham sido explorados ou a profundidade máxima seja atingida. Se o nó objetivo não for encontrado dentro da profundidade máxima, o programa imprime uma mensagem indicando isso.

class Node:
    def __init__(self, name):
        self.children = []
        self.name = name

    def add_child(self, node):
        self.children.append(node)


def DLS(node, goal, depth, path):
    print('Profundidade:', depth, 'Nó atual:', node.name)
    path.append(node.name)
    if depth == 0 and node.name == goal:
        return path
    elif depth > 0:
        for child in node.children:
            result = DLS(child, goal, depth-1, path)
            if result is not None:
                return result
            path.pop()
    return None


def IDDFS(root, goal, max_depth):
    for depth in range(max_depth):
        path = []
        result = DLS(root, goal, depth, path)
        if result is not None:
            return result
    return None


# Criação do grafo
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

# Execução da busca
goal = 'F'
max_depth = 3
result = IDDFS(root, goal, max_depth)

if result is not None:
    # print('Caminho até o nó objetivo:', ' -> ATUMALACA '.join(result))
    print(result)
else:
    print('Nó objetivo não encontrado dentro da profundidade máxima')
