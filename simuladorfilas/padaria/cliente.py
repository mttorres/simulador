class Cliente(object):
    numeroDeInstancias = 0
    def __init__(self):
        self.numero = Cliente.numeroDeInstancias
        Cliente.numeroDeInstancias += 1
        self.a_pagar = 0

    def __str__(self):
        return "cliente"+str(self.numero)+" conta: "+str(self.a_pagar)