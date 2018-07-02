from padaria.cliente import Cliente
from padaria.padaria import Padaria
from evento.evento import Evento
from gerador.gerador import conglinear, geraexp, unconglinear, geraexpdiscret, geradoreventos
import time
# OBS'S: criar uma classe padaria? que guarda informações relevantes tipo o lucro total... etc ou as filas?
#estados: definido pelo N das filas
# eventos: CHEGADA,SAIDA,DESISTIU(?), DE UMA FILA EM UM CERTO TEMPO

# parametros:
# ambos sao exponenciais, valores esperado de uma variavel exponencial = 1/lambda
EX = 90 #  lembrando que ele quer que usemos E[X] = 90 ms como parametro (tempo medio para servir uma requisição)(lambda = 1/90 é aproximadamente 11 se a unidade for segundos)
EC = 110 # lembrando que ele quer quer que usemos E[C] = 110 ms como parametro(intervalo de tempo medio entre chegadas(lambda= 1/100 é aproximadamente 9 se a unidade for segundos)
## USADOS PARA TESTE!##
vetuni = []
s = 5
qtd = 5
conglinear(13445,0,2**31-1,s,vetuni,qtd) # testando com 5 numeros e semente 5
expat = geraexp(1/110,vetuni) # tempos de chegada da fila atendimento
exppa = geraexp(1/90,vetuni) # tempos de saida da fila de atendimento e entrada da fila pagamento
# USADO PARA O TESTE NUMEROS INTEIROS DE CHEGADAS!!:
geraexpdiscret(exppa)
geraexpdiscret(expat)

#medidas de interesse
EW = 0 # tempo medio que permanece no sistema
ED = 0 # taxa de descarte (desistencias)?
EDD = 0 # taxa de descarte mesmo K == 15?
EK = 0 # tamanho medio da fila
# lista de eventos
# "setando o inicio" (bootstrap como ta no slide)
padaria = Padaria()
le = []
evento0 = Evento(0,1) # evento de chegada inicial, na fila de atendimento 1
le.append(evento0) # eventos SAO ORDENADAOS POR ORDEM DE OCORRENCIA!
# contador minutos(loop da simulação)
timeLoop = True
seg = 0
mins = 0
tempomax = 60 # MINUTOS tempo de simulação (nao é realmente necessário ser tempo real)
N = 0  # total de pessoas na padaria (todas as filas)
NC = 0 # total de chegadas (1a fila)
NS = 0 # total de saidas   (2a fila)
# os ns de cada fila podem ser checados pelo atributo ou por um metodo e sao sempre alterados dentro do loop


# loop da simulação
K = 15
while timeLoop:
        prioridade = round(unconglinear(13445,0,2**(31-1))) # gera uma prioridade aleatoria 0 ou 1
        print("prioridade: ",prioridade)
        mins += 1
        print(str(mins) + " Mins ")
     #   time.sleep(1)
        if (len(le) > 0 and le[0].tempo == mins): # evento que esta acontecendo agora
           if(le[0].tipo == 0):  # é um evento de chegada
                print("cheguei!")  # atendimento
                c = Cliente(prioridade)
                print(c)  # o cliente que chegou
                NC += 1
                N +=1
                if(c.prioridade == 1):
                    if(padaria.pessoasemfila(1) < K):
                        print("pessoas na fila A1: ", padaria.pessoasemfila(1))
                        padaria.FA1.append(c)
                        print("pessoas na fila A1: ",padaria.pessoasemfila(1))
                    elif(padaria.pessoasemfila(2) < K):
                        padaria.FA2.append(c)
                    elif(padaria.pessoasemfila(3) == 0):
                        padaria.FAP.append(c)

                    else:
                        N = N-1
                        print("DESCARTE")

                if(c.prioridade == 0):
                        if(padaria.pessoasemfila(3) < K ):
                            padaria.FAP.append(c) # OBS aqui temos que fazer a verificação se tem alguem nao prioritario na fila...
                        elif (padaria.pessoasemfila(1) < K):
                            padaria.FA1.append(c)
                        elif (padaria.pessoasemfila(2) < K):
                            padaria.FA2.append(c)
                        else:
                            N = N - 1
                            print("DESCARTE")
                # gerar evento de SAIDA DESSA FILA, e outra entrada nessa dessa mesma
                evento1 = geradoreventos(exppa,1,mins)
                evento2 = geradoreventos(expat, 0, mins)
                if(evento1.tempo > evento2.tempo):
                    le.append(evento2)
                    le.append(evento1)
                else:
                    le.append(evento1)
                    le.append(evento2)
           elif(le[0].tipo == 1):   # saida
                    NS += 1
                    N = N - 1
                    print("saida") # tem que tirar de uma das filas... POR ISSO É COMPLICADO, temos que escolher uma das 3
                    # gerar evento de chegada na fila 2
           le.remove(le[0])




        if mins == 200: # teste....
            print("Simulação terminada")
            print(padaria.FA1) # seria interessante criar um metodo str para o cliente para o print nao ficar feio kkk e facilitar debugar
            print(padaria.FA2)
            print(le) # tem que terminar vazia
            break


