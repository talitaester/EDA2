def processar_arquivo_entrada(nome_entrada, nome_saida):
    with open(nome_entrada, 'r') as arquivo:
        conteudo = arquivo.read()
    
    # Divide os números por espaço e converte para inteiros
    numeros = conteudo.split()

    # Escreve um número por linha no arquivo de saída
    with open(nome_saida, 'w') as arquivo_saida:
        for numero in numeros:
            arquivo_saida.write(numero.strip() + '\n')

if __name__ == "__main__":
    processar_arquivo_entrada('input2.txt', 'saida.txt')
