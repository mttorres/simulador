class Evento(object):
    numeroDeInstancias = 0
    def __init__(self,chegada,saida,desis,tempo,fila):
        Evento.numeroDeInstancias += 1  # é para nao precisarmos dar nome para cada evento xD
        self.tempo = tempo # tempo de chegada ou de qualquer uma das outras coisas
        self.fila = fila
        # flag para cada evento
        self.chegada = chegada
        self.saida = saida
        self.desis = desis
