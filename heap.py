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
