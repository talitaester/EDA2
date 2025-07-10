import os
import sys
import tempfile
import shutil
from heap import MinHeapSelecao  # <- sua heap personalizada

def ler_registro(arquivo):
    linha = arquivo.readline()
    if not linha:
        return None
    try:
        return int(linha.strip())
    except ValueError:
        return None

def selecao_por_substituicao(p, arquivo_entrada):
    runs = []
    heap = MinHeapSelecao()

    with open(arquivo_entrada, 'r') as entrada:
        # Inicializa heap com os primeiros p elementos válidos
        while len(heap) < p:
            num = ler_registro(entrada)
            if num is not None:
                heap.push(num)
            else:
                break
        
        # Enquanto houver elementos na heap
        while len(heap) > 0:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as run_file:
                runs.append(run_file.name)
                ultimo = -float('inf')

                while not heap.todos_marcados():
                    reg = heap.pop()
                    run_file.write(f"{reg.valor}\n")
                    ultimo = reg.valor

                    novo = ler_registro(entrada)
                    if novo is not None:
                        if novo >= ultimo:
                            heap.push(novo)
                        else:
                            heap.push(novo, marcado=True)

                # Se restaram itens marcados, remove marcação e prepara para próxima run
                remanescentes = []
                while len(heap) > 0:
                    reg = heap.pop()
                    remanescentes.append((reg.valor, False))  # desmarcar

                for valor, marcado in remanescentes:
                    heap.push(valor, marcado)

    return runs


def pway_merge(runs, p, arquivo_saida):
    import heapq  # OK usar heapq aqui, não há marcação

    passagens = 0

    while len(runs) > 1:
        novas_runs = []

        for i in range(0, len(runs), p):
            grupo = runs[i:i+p]
            if not all(os.path.exists(run) for run in grupo):
                raise FileNotFoundError("Arquivo de run não encontrado")

            with tempfile.NamedTemporaryFile(mode='w', delete=False) as run_saida:
                arquivos = [open(run, 'r') for run in grupo]
                heap = []

                for idx, arq in enumerate(arquivos):
                    num = ler_registro(arq)
                    if num is not None:
                        heapq.heappush(heap, (num, idx))

                while heap:
                    menor, idx = heapq.heappop(heap)
                    run_saida.write(f"{menor}\n")
                    num = ler_registro(arquivos[idx])
                    if num is not None:
                        heapq.heappush(heap, (num, idx))

                for arq in arquivos:
                    arq.close()
                novas_runs.append(run_saida.name)

        for run in runs:
            try:
                os.remove(run)
            except:
                pass

        runs = novas_runs
        passagens += 1

    if runs:
        shutil.copyfile(runs[0], arquivo_saida)
        os.remove(runs[0])

    return passagens


def main():
    if len(sys.argv) != 4:
        print("Uso: python pways.py <p> <entrada.txt> <saida.txt>")
        return
    p = int(sys.argv[1])
    arquivo_entrada = sys.argv[2]
    arquivo_saida = sys.argv[3]

    runs = selecao_por_substituicao(p, arquivo_entrada)
    num_passagens = pway_merge(runs, p, arquivo_saida)

    total_registros = sum(1 for linha in open(arquivo_entrada) if linha.strip().isdigit())
    print(f"#Regs Ways #Runs #Parses")
    print(f"{total_registros} {p} {len(runs)} {num_passagens}")

if __name__ == "__main__":
    main()
