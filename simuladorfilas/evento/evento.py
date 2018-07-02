class Evento(object):
    numeroDeInstancias = 0
    def __init__(self,tipo,tempo,fila):
        self.numero = Evento.numeroDeInstancias
        Evento.numeroDeInstancias += 1  # é para nao precisarmos dar nome para cada evento xD
        self.tempo = tempo # tempo de chegada ou de qualquer uma das outras coisas
        self.fila = fila # codigo da fila 1 ou 2
        # MUDANÇA: é uma flag só
        self.tipo = tipo # 0(chegada),1(saida) 2 (desistencia)




    def __str__(self):
        return "evento"+str(self.numero) + "tipo"+str(self.tipo)