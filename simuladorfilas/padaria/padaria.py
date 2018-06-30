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