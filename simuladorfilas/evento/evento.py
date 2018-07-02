class Evento(object):
    numeroDeInstancias = 0
    def __init__(self,tipo,tempo,fila):
        self.numero = Evento.numeroDeInstancias
        Evento.numeroDeInstancias += 1  # é para nao precisarmos dar nome para cada evento xD
        self.tempo = tempo # tempo de chegada
        self.cheg = -1 # se for -1 é pq é um evento de chegada ( ou seja o tempo já é igual a chegada) , caso contrario é de saida
        # onde é interesseante guardar o intervalo saida - chegada
        self.fila = fila # codigo da fila 1 ou 2

        # MUDANÇA: é uma flag só
        self.tipo = tipo # 0(chegada),1(saida) 2 (desistencia)


    def setacheg(self,t):
        if(self.tipo == 1):
            self.cheg = t
        else:
            self.cheg = -1
            print("erro")

    def __str__(self):
        return "evento"+str(self.numero) + "tipo"+str(self.tipo)+ " ocorre em: "+str(self.tempo)