from padaria.cliente import Cliente
from padaria.padaria import Padaria
from evento.evento import Evento
import time
# OBS'S: criar uma classe padaria? que guarda informações relevantes tipo o lucro total... etc ou as filas?
#estados: definido pelo N das filas


# eventos: CHEGADA,SAIDA,DESISTIU(?), DE UMA FILA EM UM CERTO TEMPO

# lista de eventos
# "setando o inicio" (bootstrap como ta no slide)
padaria = Padaria()
eventoqualquer = Evento(1,0,0,4,padaria.FA1)
#clientequalquer = Cliente(1)
le = []
le.append(eventoqualquer) # eventos SAO ORDENADAOS POR ORDEM DE OCORRENCIA!

# contador minutos
timeLoop = True
seg = 0
mins = 0
tempomax = 60 # MINUTOS tempo de simulação (nao é realmente necessário ser tempo real)
# testes  com o time
''' #TESTE
while timeLoop:
        seg += 1
        print(str(mins) + " Mins " + str(seg) + " Segs ")
        time.sleep(1)
        if seg == 60:
            Sec = 0
            mins += 1
            print(str(mins) + " minutos")

'''
# teste mais basico de todos?
K = 5
while timeLoop:
        mins += 1
        print(str(mins) + " Mins ")
        time.sleep(1)
        if (len(le) > 0 and le[0].tempo == mins):
           print("cheguei!")  # atendimento
           c = Cliente(1)
           if(c.prioridade == 1):
               if(len(padaria.FA1) == K):
                   padaria.FA2.append(c)
               else:
                   padaria.FA1.append(c)
           # remover da lista de eventos... o evento de chegada aos ao tempo tal
           le.remove(le[0])
           # ADICIONAR NOVO EVENTO
        if mins == 60:
            print("Simulação terminada")
            print(padaria.FA1) # seria interessante criar um metodo str para o cliente para o print nao ficar feio kkk e facilitar debugar
            print(padaria.FA2)
            print(le) # tem que terminar vazia
            break


