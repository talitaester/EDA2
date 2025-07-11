import os
import sys
import tempfile
import shutil
import heapq

class Registro:
    def __init__(self, valor, marcado=False, origem=None):
        self.valor = valor
        self.marcado = marcado
        self.origem = origem  

    def __lt__(self, outro):
        if self.marcado != outro.marcado:
            return not self.marcado and outro.marcado
        return self.valor < outro.valor

    def __repr__(self):
        marca = "*" if self.marcado else ""
        origem = f"({self.origem})" if self.origem is not None else ""
        return f"{marca}{self.valor}{origem}"

class MinHeapSelecao:
    def __init__(self):
        self.heap = []

    def push(self, valor, marcado=False, origem=None):
        heapq.heappush(self.heap, Registro(valor, marcado, origem))

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)
        return None

    def peek(self):
        return self.heap[0] if self.heap else None

    def __len__(self):
        return len(self.heap)

    def todos_marcados(self):
        return all(reg.marcado for reg in self.heap)

    def heapify(self):
        heapq.heapify(self.heap)


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
    passagens = 0

    while len(runs) > 1:
        novas_runs = []

        for i in range(0, len(runs), p):
            grupo = runs[i:i+p]
            if not all(os.path.exists(run) for run in grupo):
                raise FileNotFoundError("Arquivo de run não encontrado")

            with tempfile.NamedTemporaryFile(mode='w', delete=False) as run_saida:
                arquivos = [open(run, 'r') for run in grupo]
                heap = MinHeapSelecao()

                # Inicializa heap com primeiro valor de cada run
                for idx, arq in enumerate(arquivos):
                    num = ler_registro(arq)
                    if num is not None:
                        heap.push(num, origem=idx)  # origem = índice do arquivo

                while len(heap) > 0:
                    reg = heap.pop()
                    run_saida.write(f"{reg.valor}\n")
                    novo = ler_registro(arquivos[reg.origem])
                    if novo is not None:
                        heap.push(novo, origem=reg.origem)

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