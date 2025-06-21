import random

def gerar_arquivo_aleatorio(nome_arquivo, quantidade, valor_min=1, valor_max=1000000):
    """
    Gera um arquivo com 'quantidade' números aleatórios entre 'valor_min' e 'valor_max'.
    Cada número em uma linha.
    """
    with open(nome_arquivo, 'w') as arquivo:
        for _ in range(quantidade):
            num = random.randint(valor_min, valor_max)
            arquivo.write(f"{num}\n")

if __name__ == "__main__":
    nome_arquivo = "input.txt"  # Nome do arquivo de saída
    quantidade_numeros = 2_000_000      # Altere este valor conforme desejado (~70MB com 10 milhões de números)
    
    gerar_arquivo_aleatorio(nome_arquivo, quantidade_numeros)
    print(f"Arquivo '{nome_arquivo}' gerado com {quantidade_numeros} números.")
