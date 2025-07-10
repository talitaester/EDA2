import heapq

class Registro:
    def __init__(self, valor, marcado=False):
        self.valor = valor
        self.marcado = marcado

    def __lt__(self, outro):
        # Elementos não marcados têm prioridade
        if self.marcado == outro.marcado:
            return self.valor < outro.valor
        return not self.marcado and outro.marcado

    def __repr__(self):
        return f"{'*' if self.marcado else ''}{self.valor}"


class MinHeapSelecao:
    def __init__(self):
        self.heap = []

    def push(self, valor, marcado=False):
        heapq.heappush(self.heap, Registro(valor, marcado))

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
