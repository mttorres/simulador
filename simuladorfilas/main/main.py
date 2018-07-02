from padaria.cliente import Cliente
from padaria.padaria import Padaria
from evento.evento import Evento
from gerador.gerador import conglinear, geraexp, unconglinear, geraexpdiscret
import time
# OBS'S: criar uma classe padaria? que guarda informações relevantes tipo o lucro total... etc ou as filas?
#estados: definido pelo N das filas
# eventos: CHEGADA,SAIDA,DESISTIU(?), DE UMA FILA EM UM CERTO TEMPO

# parametros:
# ambos sao exponenciais, valores esperado de uma variavel com distribuição exponencial = 1/lambda
EX = 90 #  lembrando que ele quer que usemos E[X] = 90 ms como parametro (tempo medio para servir uma requisição)(lambda = 1/90 é aproximadamente 11 se a unidade for segundos)
EC = 110 # lembrando que ele quer quer que usemos E[C] = 110 ms como parametro(intervalo de tempo medio entre chegadas(lambda= 1/100 é aproximadamente 9 se a unidade for segundos)
## USADOS PARA TESTE!##
vetuni = [] # vetor unitario com x numeros entre 0 e 1
s = 5
qtd = 5
conglinear(13445,0,2**31-1,s,vetuni,qtd) # testando com 5 numeros e semente 5
expat = geraexp(1/110,vetuni) # tempos de chegada da fila atendimento
exppa = geraexp(1/90,vetuni) # tempos de saida da fila de atendimento e entrada da fila pagamento
# USADO PARA O TESTE NUMEROS INTEIROS DE CHEGADAS!!:
geraexpdiscret(exppa)
geraexpdiscret(expat)

#medidas de interesse
EWi1 = 0 # tempo medio que uma requisição permanece no sistema (somar o tempo de permanencia(saida - chegada) de todos)(fila1)
EWi2 = 0 #
EWt = 0 # EWi1 + probdesistenciaxEWi2
ED = 0 # taxa de descarte (desistencias)?
EDD = 0 # taxa de descarte mesmo K == 15?
EK1 = 0 # tamanho medio da fila 1
EK2 = 0 # tamanho medio da fila 2
utilizacaof1 = 0 # utilização do recurso?
utilizacaof2 = 0
# lista de eventos
# "setando o inicio" (bootstrap como ta no slide)
padaria = Padaria()
le = []
evento0 = Evento(0,1,1) # evento de chegada inicial, na fila de atendimento 1
le.append(evento0) # eventos SAO ORDENADAOS POR ORDEM DE OCORRENCIA!
# contador minutos(loop da simulação)
timeLoop = True
seg = 0
mins = 0    # por quanto tempo devemos por ja que ele botou mili segundos!?
tempomax = 60000 # coloquei 60 mil por enquanto
#tempomax = 3600000 # 60 MINUTOS tempo de simulação (nao é realmente necessário ser tempo real)
N = 0  # total de pessoas na padaria (todas as filas)
NC = 0 # total de chegadas (1a fila) ( e consequentemente ao sistema)
NS = 0 # total de saidas  fila 1 # pode desistir dps da fila 1
NC2 = 0 # total de chegadas a fila 2 (nao desistiu)
NS2 = 0 # total saidas fila 2
NSS = 0 # numero de saidas do sistema
# os ns de cada fila podem ser checados pelo atributo ou por um metodo e sao sempre alterados dentro do loop


# loop da simulação
K = 15
while timeLoop:
    mins+=1
    if (len(le) > 0 and le[0].tempo == mins):
        if (le[0].tipo == 0):  # é um evento de chegada
            print("cheguei!")
            c = Cliente()
            if (padaria.pessoasemfila(1) < K):
                N += 1
                NC+= 1
                padaria.FA1.append(c)
                #gerar proxima chegada(outro cara) e a saida desse que chegou agora(que é tmb a chegada na fila 2)
                # e adicionar a lista de eventos
            else:
                print("descarte")
                EDD = EDD + 1 # contando os descartes e dps fazer a media no final do programa EDD/total de chegadas
        if(le[0].tipo == 1 and le[0].fila == 1): # evento de saida da fila 1 (e chegada na fila2)
             print("saida fila 1!")
             #N-= 1 NA VDD ELE CONTINUA NO SISTEMA
             NS+=1
             if (padaria.pessoasemfila(2) < K):
                NC2 += 1
                cliente = padaria.FA1.popleft() # devolve o cara que saiu dessa fila... # e que deve entrar na segunda fila!
                cliente.a_pagar = 9.50 # um valor qualquer para pagar
                padaria.FP1.append(s)
                # gerar a saida desse cara da fila 2
             else:
                print("desistiu") # ou descarte da fila 2

        if (le[0].tipo == 1 and le[0].fila == 2):
            print("saida fila 2!(da padaria)")
            NS2-= 1
            NSS+= 1



        le.remove(le[0]) # removendo o evento atual

    if mins == tempomax:  # teste....
        print("Simulação terminada")
       # print(padaria.FA1)  # seria interessante criar um metodo str para o cliente para o print nao ficar feio kkk e facilitar debugar
       # print(padaria.FA2)
        print(le)  # tem que terminar vazia
        break