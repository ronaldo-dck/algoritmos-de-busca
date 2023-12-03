import subprocess

def salvar_dados(partida, dados, nome_arquivo):
    # Aqui você implementa a lógica para salvar os dados em um arquivo
    # Neste exemplo, estou abrindo o arquivo em modo de escrita e escrevendo os dados
    with open(nome_arquivo, 'a') as file:
        file.write(f"Partida: {partida}, Dados: {dados}\n")

def executar_teste(partida, entrada, nome_arquivo):
    # Aqui você deve chamar o connect4 com a combinação de entrada (I/A)
    print(f"Executando teste para Partida {partida} com entrada {entrada}")

    # Subprocesso para chamar o connect4 e redirecionar a saída para um arquivo
    with open(nome_arquivo, 'a') as file:
        subprocess.run(["py connect4.py"], stdout=file, text=True)

# Exemplo de como você pode usar as funções
if __name__ == "__main__":
    partidas = ["Partida1", "Partida2", "Partida3"]
    entradas = ["I", "A"]

    for n, partida in enumerate(partidas, start=1):
        for entrada in entradas:
            # Nome do arquivo de saída
            nome_arquivo = f"fout_file{n}.txt"

            # Chamada da função para executar o teste
            executar_teste(partida, entrada, nome_arquivo)

            # Dados simulados que você deseja salvar
            dados = {"campo1": "valor1", "campo2": "valor2"}

            # Chamada da função para salvar os dados
            salvar_dados(partida, dados, nome_arquivo)
