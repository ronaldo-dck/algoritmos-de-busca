import networkx as nx

def criar_tabuleiro_vazio():
    return [[0] * 7 for _ in range(6)]

def copiar_tabuleiro(tabuleiro):
    return [row[:] for row in tabuleiro]

def imprimir_tabuleiro(tabuleiro):
    for row in tabuleiro:
        print(row)
    print()

def realizar_jogada(tabuleiro, coluna, jogador):
    for i in range(5, -1, -1):
        if tabuleiro[i][coluna] == 0:
            tabuleiro[i][coluna] = jogador
            return tabuleiro

def verificar_vitoria(tabuleiro, jogador):
    # Verifica se há uma vitória na horizontal, vertical ou diagonal
    for i in range(6):
        for j in range(4):
            # Verifica na horizontal
            if tabuleiro[i][j] == tabuleiro[i][j+1] == tabuleiro[i][j+2] == tabuleiro[i][j+3] == jogador:
                return True
            # Verifica na vertical
            if tabuleiro[j][i] == tabuleiro[j+1][i] == tabuleiro[j+2][i] == tabuleiro[j+3][i] == jogador:
                return True
    # Verifica nas diagonais
    for i in range(3):
        for j in range(4):
            if tabuleiro[i][j] == tabuleiro[i+1][j+1] == tabuleiro[i+2][j+2] == tabuleiro[i+3][j+3] == jogador:
                return True
            if tabuleiro[i][j+3] == tabuleiro[i+1][j+2] == tabuleiro[i+2][j+1] == tabuleiro[i+3][j] == jogador:
                return True
    return False

def calcular_movimentos_minimos(tabuleiro):
    # Neste exemplo, uma heurística simples é utilizada
    # Conta o número de peças no tabuleiro
    return sum(row.count(1) + row.count(2) for row in tabuleiro)

def gerar_grafo_profundidade_limitada(tabuleiro_inicial, profundidade):
    G = nx.Graph()

    def dfs(tabuleiro, atual_profundidade, jogador):
        if atual_profundidade == 0:
            return

        for coluna in range(7):
            novo_tabuleiro = copiar_tabuleiro(tabuleiro)
            novo_tabuleiro = realizar_jogada(novo_tabuleiro, coluna, jogador)
            
            # Avalia a quantidade mínima de movimentos usando a heurística
            movimentos_minimos = calcular_movimentos_minimos(novo_tabuleiro)

            G.add_edge(str(tabuleiro), str(novo_tabuleiro), weight=movimentos_minimos)
            dfs(novo_tabuleiro, atual_profundidade - 1, 3 - jogador)  # Alterna entre jogadores

    G.add_node(str(tabuleiro_inicial))
    dfs(tabuleiro_inicial, profundidade, 1)

    return G

# Exemplo de uso:
tabuleiro_inicial = criar_tabuleiro_vazio()
profundidade_limite = 6
grafo = gerar_grafo_profundidade_limitada(tabuleiro_inicial, profundidade_limite)

# Exibe informações sobre o grafo gerado
print("Número de nós:", grafo.number_of_nodes())
print("Número de arestas:", grafo.number_of_edges())

# Para visualizar o grafo, você pode usar ferramentas como o Graphviz
# por exemplo, você pode exportar o grafo para um arquivo DOT e visualizá-lo usando Graphviz
# nx.write_dot(grafo, "connect4_graph.dot")
# Certifique-se de ter o Graphviz instalado e execute o seguinte comando no terminal:
# dot -Tpng connect4_graph.dot -o connect4_graph.png
