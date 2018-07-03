from collections import deque
class Padaria(object):
    def __init__(self):
        self.deveriareceber = 0 # o quanto ele recebeu efetivamente já que as pessoas desistiram
        self.recebeu = 0   #  o quanto ele recebeu de dinheiro (capital)
        #filas
        self.FA1 = deque([])  # entrada 1 atendimento

        self.FP1 = deque([])  # entrada 1 pagamento

    def pessoasemfila(self, cod):
        if cod == 1:
            return len(self.FA1)
        if cod == 2:
            return len(self.FP1)
        else:
            return -1
