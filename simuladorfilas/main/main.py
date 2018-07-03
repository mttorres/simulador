import sys
sys.path.append('../')
from padaria.cliente import Cliente
from padaria.padaria import Padaria
from evento.evento import Evento
from gerador.gerador import conglinear, geraexp, unconglinear, geraexpdiscret,ungeraexp


#estados: definido pelo N das filas
# eventos: CHEGADA,SAIDA,DESISTIU, DE UMA FILA EM UM CERTO TEMPO

# parametros:
# o a fila 1 chegada a cada 110ms, processamento 90 ms, fazendo a fila 2 ter chegada 90ms
EC = 110
EX = 90
#EC = int(input("EC: "))   experimento
tempomax = 3600000 #60min simulacao

# VETORES DE NUMEROS ALEATORIOS ENTRE 0 E 1
vetuni = [] # vetor unitario com x numeros entre 0 e 1 # ~32 mil numeros (chegada fila 1)
conglinear(13445,0,2**31-1,5000,vetuni,tempomax//EC)
vetuni.sort()
vetuni2 =[] # 40 mil numeros (saida fila 1) e chegada fila 2
conglinear(13445,0,2**31-1,15000,vetuni2,tempomax//EX)
vetuni2.sort()
vetuni3 = [] # ~42 mil numeros (saida fila 2)
conglinear(13445,0,2**31-1,20000,vetuni3,tempomax//85)
vetuni3.sort()

#medidas de interesse
EWi1 = 0 # tempo medio que uma requisição permanece no sistema
EWi2 = 0 
EWt = 0 # EWt1 + probdesistenciaxEWt2
ED = 0 # taxa de descarte (desistencias)
EDD = 0 # taxa de descarte mesmo K == 15
EK1 = 0 # tamanho medio da fila 1
EK2 = 0 # tamanho medio da fila 2
utilizacaof1 = (1/EC)*EX # utilização do recurso? é simplesmente lambda*e[x] de cada fila usaremos para o grafico só
utilizacaof2 = (1/EX)*85

# lista de eventos
# "setando o inicio" (bootstrap como ta no slide)
padaria = Padaria()
listaEventos = []
evento0 = Evento(0,ungeraexp(1/EC,vetuni[0]),1) # evento de chegada inicial, na fila 1
vetuni.remove(vetuni[0]) # remove esse tempo (nao pode chegar outro cara exatamente nesse mesmo tempo!)
listaEventos.append(evento0) # eventos SAO ORDENADAOS POR ORDEM DE OCORRENCIA
timeLoop = True # contador minutos(loop da simulação)
tempoDecorrido = 0 # tempo decorrido ate agora
N = 0  # total de pessoas na padaria (todas as filas)
NC = 0 # total de chegadas (1a fila) ( e consequentemente ao sistema)
NS = 0 # total de saidas  fila 1 # pode desistir dps da fila 1
NC2 = 0 # total de chegadas a fila 2 (nao desistiu)
NS2 = 0 # total saidas fila 2
NSS = 0 # numero de saidas do sistema



# loop da simulação
K = 15
while timeLoop:
    #print("minutos: ",tempoDecorrido)
    if (tempoDecorrido >= tempomax):
        timeLoop = False
        break

    if (len(listaEventos) > 0 ): # tem evento para acontecer
        if (listaEventos[0].tipo == 0 and (tempoDecorrido <= listaEventos[0].tempo <= tempoDecorrido+1)):  # é um evento de chegada
            print("Chegou um evento!")
            print("Tempo de chegada:",listaEventos[0].tempo)
            c = Cliente()
            N += 1
            NC+= 1
            if (padaria.pessoasemfila(1) < K):
                padaria.FA1.append(c) # jogou na fila 1
                #gerar proxima chegada e a saida desse que chegou agora
                eventoChegada = Evento(0, ungeraexp(1 / EC, vetuni[0]), 1)
                eventoSaida = Evento(1, ungeraexp(1 / EX, vetuni2[0])+listaEventos[0].tempo, 1) # salva o tempo de saida(chegada + o tempo gerado)
                eventoSaida.setacheg(listaEventos[0].tempo) # salva o tempo de chegada e temos agora o intervalo (saida - chegada)
                vetuni.remove(vetuni[0]) # remove da lista de valores 0,1 para nao ter repetições
                vetuni2.remove(vetuni2[0])
                listaEventos.append(eventoChegada)
                listaEventos.append(eventoSaida)
                #adicionar a lista de eventos
                listaEventos.sort(key=lambda evento: evento.tempo) # ordenada a lista de eventos
            else:
                print("descarte")
                EDD = EDD + 1 # contando os descartes e dps fazer a media no final do programa EDD/total de chegadas
            #independente do descarte ou nao a chegada aconteceu e deve ser removida da lista e o tempo tempoDecorrido atualizado
            tempoDecorrido = listaEventos[0].tempo
            listaEventos.remove(listaEventos[0])  # removendo o evento atual
         #   print("minutos: ", tempoDecorrido)
                                                                                                    # esse evento acontece efetivamente após chegada + saida
        elif(listaEventos[0].tipo == 1 and listaEventos[0].fila == 1 and (tempoDecorrido <= listaEventos[0].tempo <= tempoDecorrido+1)): # evento de saida da fila 1 (e chegada na fila2)
             print("saida fila 1!")
             NS+=1 # saida da fila 1
             EWi1 += listaEventos[0].tempo - listaEventos[0].cheg # (saida - chegada) (intervalo efetivo) de cada elemento na fila 1
             padaria.deveriareceber += 1.00 # deveria receber um valor de +1.00$
             if (padaria.pessoasemfila(2) < K and padaria.pessoasemfila(1) > 0):
                # processar o evento de saida da fila 1!
                NC2 += 1
                cliente = padaria.FA1.popleft() # devolve o cara que saiu dessa fila... # e que deve entrar na segunda fila!
                cliente.a_pagar = 1.00 # um valor qualquer para pagar
                padaria.FP1.append(cliente)
                # gerar a saida desse cara da fila 2
                eventoSaida = Evento(1, ungeraexp(1/85, vetuni3[0])+listaEventos[0].tempo, 2)
                eventoSaida.setacheg(listaEventos[0].tempo)
                vetuni3.remove(vetuni3[0])
                listaEventos.append(eventoSaida)
                listaEventos.sort(key=lambda evento: evento.tempo)
             else:
                print("desistiu") # ou descarte da fila 2
                ED = ED+1 # "calote" (descarte da fila 2)

             listaEventos.remove(listaEventos[0])  # removendo o evento atual
          #   print("minutos: ", tempoDecorrido)

        elif (listaEventos[0].tipo == 1 and listaEventos[0].fila == 2 and (tempoDecorrido <= listaEventos[0].tempo <= tempoDecorrido+1)):
            EWi2 += listaEventos[0].tempo - listaEventos[0].cheg  # (saida - chegada) (intervalo efetivo)
            if (padaria.pessoasemfila(2)  > 0):
                print("saida fila 2!( e da padaria)")
                N -= 1 # 1 saida do sistema (total de pessoas no sistema diminui)
                NS2+= 1 # uma saida da fila 2
                NSS+= 1 # adiciona uma saida do sistema
                cliente = padaria.FP1.popleft()
                padaria.recebeu += cliente.a_pagar  # padaria recebeu + 9.50
            else:
                print("isso nao deveria acontecer")
                print("ele nao deveria tentar remover alguem da fila 2 sem ter ninguem!?")
            listaEventos.remove(listaEventos[0])  # removendo o evento atual
           # print("minutos: ", tempoDecorrido)

    elif(len(listaEventos)==0):
        tempoDecorrido = tempomax # nao tem evento na lista
        print("Tempo decorrido em minutos: ", tempoDecorrido/60000)

print("simulação encerrada!")
print("total de chegadas a padaria/fila1: ",NC)
print("total de saidas da fila1", NS)
print("total de chegadas a fila da fila2", NS2)
print("total de saidas da padaria: ", NSS)
print("total de descarte em f1: ", EDD)
print("total de CALOTES em f2: ", ED)
print("Prejuizo: ", padaria.recebeu - padaria.deveriareceber)
print("tempo medio que uma requisição permanece em f1",EWi1/(NC-EDD)) # tempo de cada requisição menos as descartadas
print("tempo medio que uma requisição permanece em f2",EWi2 / (NC2 - ED))  # tempo de cada requisição menos as desistencias