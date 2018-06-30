class Cliente(object):
    numeroDeInstancias = 0
    def __init__(self,prioridade):
        Cliente.numeroDeInstancias += 1 # é para nao precisarmos dar nome para cada cliente xD
        self.prioridade = prioridade
        self.a_pagar = 0

        # algo mais...?