from collections import deque
from padaria.cliente import Cliente
class Padaria(object):
    def __init__(self):
        self.deveriareceber = 0 # o quanto ele recebeu efetivamente já que as pessoas desistiram
        self.recebeu = 0   #  o quanto ele recebeu de dinheiro (lucro)
        #filas
        self.FA1 = deque([])  # entrada 1 atendimento
        self.FA2 = deque([])  # entrada 2 atendimento
        self.FAP = deque([])  # entrada prioritaria atendimento

        self.FP1 = deque([])  # entrada 1 pagamento
        self.FPP = deque([])  # entrada prioritaria pagamento




    # METODOS? CHEGADA , SAIDA ?
    # codigo da fila
    def pessoasemfila(self,cod):
        if cod == 1:
            return len(self.FA1)
        if cod == 2:
            return len(self.FA2)
        if cod == 3:
            return len(self.FAP)
        if cod == 4:
            return len(self.FP1)
        if cod == 5:
            return len(self.FP1)

