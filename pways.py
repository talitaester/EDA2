import heapq
import os
import sys
import tempfile

def ler_registro(arquivo):
    linha = arquivo.readline()
    if not linha:
        return None
    try:
        return int(linha.strip())
    except ValueError:
        return None

def selecao_por_substituicao(p, arquivo_entrada):
    runs = [] #nomes dos arquivos temporarios criados durante a ordenação
    heap = [] #valores para serem inseridos na heap 


    #vai guardar os valores menores do que aqueles ja escritos na run atual    
    #normalmente esses valores seriam inseridos na heap como marcados****
    buffer = []
    
    with open(arquivo_entrada, 'r') as entrada:
        # Inicializa heap com os primeiros p elementos válidos
        while len(heap) < p:
            num = ler_registro(entrada)
            if num is not None:
                heapq.heappush(heap, num)
            else:
                break
        
        while heap:
            # Cria novo arquivo temporário para a run atual
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as run_file:
                runs.append(run_file.name)
                ultimo = None
                
                while heap:
                    menor = heapq.heappop(heap)
                    run_file.write(f"{menor}\n")
                    ultimo = menor
                    
                    # Lê próximo registro
                    num = ler_registro(entrada)
                    if num is not None:
                        if num >= ultimo:
                            heapq.heappush(heap, num)
                        else:
                            buffer.append(num) #guarda os valores marcados para colocar no proximo arquivo temporario
                    else:
                        continue
                
                # Prepara próxima run com o buffer
                if buffer:
                    heap = buffer
                    heapq.heapify(heap)
                    buffer = []
    
    return runs


def pway_merge(runs, p, arquivo_saida):
    temp_outputs = []
    passagens = 0 
    
    while len(runs) > 1:
        novas_runs = [] 
        
        for i in range(0, len(runs), p): #separa grupos de p runs 
            grupo = runs[i:i+p]
            # Verifica se os arquivos existem
            if not all(os.path.exists(run) for run in grupo):
                raise FileNotFoundError("Arquivo de run não encontrado")
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as run_saida:
                # Abre todos os arquivos do grupo
                arquivos = [open(run, 'r') for run in grupo]
                heap = []
                
                # Inicializa heap
                for idx, arq in enumerate(arquivos):
                    num = ler_registro(arq)
                    if num is not None:
                        heapq.heappush(heap, (num, idx))
                
                # Processa o merge
                while heap:
                    menor, idx = heapq.heappop(heap)
                    run_saida.write(f"{menor}\n")
                    
                    # Lê próximo do mesmo arquivo
                    num = ler_registro(arquivos[idx])
                    if num is not None:
                        heapq.heappush(heap, (num, idx))
                
                # Fecha arquivos e armazena nova run
                for arq in arquivos:
                    arq.close()
                novas_runs.append(run_saida.name)
        
        # Remove arquivos antigos
        for run in runs:
            try:
                os.remove(run)
            except:
                pass
        
        runs = novas_runs
        passagens += 1
    
    # Move o arquivo final para o destino
    if runs:
        os.replace(runs[0], arquivo_saida)
    
    return passagens


def main():
    if len(sys.argv) != 4:
        print("Uso: python pways.py <p> <entrada.txt> <saida.txt>")
        return
    p = int(sys.argv[1])
    arquivo_entrada = sys.argv[2]
    arquivo_saida = sys.argv[3]

    runs = selecao_por_substituicao(p, arquivo_entrada)
    num_passagens = pway_merge(runs, 2*p, arquivo_saida)

    total_registros = sum(1 for _ in open(arquivo_entrada))
    print(f"#Regs Ways #Runs #Parses")
    print(f"{total_registros} {p} {len(runs)} {num_passagens}")

if __name__ == "__main__":
    main()
