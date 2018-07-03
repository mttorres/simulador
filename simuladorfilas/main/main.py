import sys
sys.path.append('../')
from padaria.cliente import Cliente
from padaria.padaria import Padaria
from evento.evento import Evento
from gerador.gerador import conglinear, geraexp, unconglinear, geraexpdiscret,ungeraexp


#estados: definido pelo N das filas
# eventos: CHEGADA,SAIDA,DESISTIU(?), DE UMA FILA EM UM CERTO TEMPO

# parametros:
# ambos sao exponenciais, valores esperado de uma variavel com distribuição exponencial = 1/lambda
# o a fila 1 chegada a cada 110ms , lambda= 1/110 e tem processamento 90 ms, fazendo a fila 2 ter chegada 1/90
EX = 90 # entrada Guto
#EC = 110 Entrada guto

EC = int(input("EC: "))
EY = int(input("EY: "))
tempomax = 3600000 # 60min simulacao

# VETORES DE NUMEROS ALEATORIOS ENTRE 0 E 1
vetuni = [] # vetor unitario com x numeros entre 0 e 1 # ~32 mil numeros (chegada fila 1)(lamb / 110)
conglinear(13445,0,2**31-1,5000,vetuni,tempomax//EC)
vetuni.sort()
vetuni2 =[] # 40 mil numeros (saida fila 1) e chegada fila 2 (usa semente maior para fazer as saidas tenderem a serem maior que as chegadas)
conglinear(13445,0,2**31-1,15000,vetuni2,tempomax//EX)
vetuni2.sort()
vetuni3 = [] # ~42 mil numeros (saida fila 2)
conglinear(13445,0,2**31-1,20000,vetuni3,tempomax//EY)
vetuni3.sort()

#medidas de interesse
EWi1 = 0 # tempo medio que uma requisição permanece no sistema
EWi2 = 0 #
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
le = []
evento0 = Evento(0,ungeraexp(1/EC,vetuni[0]),1) # evento de chegada inicial, na fila 1
vetuni.remove(vetuni[0]) # remove esse tempo (nao pode chegar outro cara exatamente nesse mesmo tempo!)
le.append(evento0) # eventos SAO ORDENADAOS POR ORDEM DE OCORRENCIA
timeLoop = True # contador minutos(loop da simulação)
mins = evento0.tempo # tempo decorrido ate agora
N = 0  # total de pessoas na padaria (todas as filas)
NC = 0 # total de chegadas (1a fila) ( e consequentemente ao sistema)
NS = 0 # total de saidas  fila 1 # pode desistir dps da fila 1
NC2 = 0 # total de chegadas a fila 2 (nao desistiu)
NS2 = 0 # total saidas fila 2
NSS = 0 # numero de saidas do sistema



# loop da simulação
K = 15
while timeLoop:
    #print("minutos: ",mins)
    if (mins >= tempomax):
        print("simulação encerrada!")
        print(le)
        print("total de chegadas a padaria/fila1: ",NC)
        print("total de saidas da fila1", NS)
        print("total de chegadas a fila da fila2", NS2)
        print("total de saidas da padaria: ", NSS)
        print("total de descarte em f1: ", EDD)
        print("total de CALOTES em f2: ", ED)
        print("Prejuizo: ", padaria.recebeu - padaria.deveriareceber)
        print("tempo medio que uma requisição permanece em f1",EWi1/(NC-EDD)) # tempo de cada requisição menos as descartadas
        print("tempo medio que uma requisição permanece em f2",EWi2 / (NC2 - ED))  # tempo de cada requisição menos as desistencias
        print("tamanho medio da fila f1:",EK1/NC)
        print("tamanho medio da fila f2:", EK2 / NC)
        print(len(vetuni))
        print(len(vetuni2))
        print(len(vetuni3))

        break
    if (len(le) > 0): # tem evento para acontecer
        print("evento atual", print(le[0]))
        if (le[0].tipo == 0 and le[0].tempo == mins ):  # é um evento de chegada que gera outras chegadas
            print("Chegou um evento!")
            print("tempo",le[0].tempo)
            c = Cliente()
            N += 1
            NC += 1                                                   # apesar que vetuni tende a se esgotar antes de vetuni2...
            if (padaria.pessoasemfila(1) < K and (len(vetuni2) > 0)):   # pode ainda gerar eventos de saida? senao nao deixa adicionar
                padaria.FA1.append(c) # jogou na fila 1
                #gerar proxima chegada(gerada sempre) e a saida desse que chegou agora
                eventosa = Evento(1, ungeraexp(1 / EX, vetuni2[0])+le[0].tempo, 1) # salva o tempo de saida(chegada + o tempo gerado)
                eventosa.setacheg(le[0].tempo) # salva o tempo de chegada e temos agora o intervalo (saida - chegada)
                vetuni2.remove(vetuni2[0])
                le.append(eventosa)
                #adicionar a lista de eventos
            elif(padaria.pessoasemfila(1) >= K):
                print("descarte")
                EDD = EDD + 1 # contando os descartes e dps fazer a media no final do programa EDD/total de chegadas

            #independente do descarte ou nao a chegada aconteceu e deve ser removida da lista e o tempo mins atualizado
            # e tambem uma nova chegada deve ser gerada

            EK1 += padaria.pessoasemfila(1) # calcular o tamanho medio
            EK2 += padaria.pessoasemfila(2) # fila 2 pode ja ter alguem e se manter durante aquele instante
            if(len(vetuni) > 0): # gera outra chegada
                eventoch = Evento(0, ungeraexp(1 / EC, vetuni[0]), 1)
                vetuni.remove(vetuni[0])  # remove da lista de valores 0,1 para nao ter repetições
                le.append(eventoch)  # adicionando os novos

            le.remove(le[0])  # removendo o evento atual
            le.sort(key=lambda evento: evento.tempo)  # ordenada a lista de eventos
            #if (len(le) > 0):
            print(le[0].tempo)
            mins = le[0].tempo # 1o da lista (proximo evento)
            print(mins)
            print(le[0].tipo)


                                                                                                    # esse evento acontece efetivamente após chegada + saida
        elif(le[0].tipo == 1 and le[0].fila == 1 and le[0].tempo == mins ): # evento de saida da fila 1 (e chegada na fila2)
             print("saida fila 1!")
             NS+=1 # saida da fila 1
             EWi1 += le[0].tempo - le[0].cheg # (saida - chegada) (intervalo efetivo) de cada elemento na fila 1
             padaria.deveriareceber += 1.00 # deveria receber um valor de +1.00$
             if (padaria.pessoasemfila(2) < K and padaria.pessoasemfila(1) > 0 and len(vetuni3) > 0):
                # processar o evento de saida da fila 1!
                NC2 += 1
                cliente = padaria.FA1.popleft() # devolve o cara que saiu dessa fila... # e que deve entrar na segunda fila!
                cliente.a_pagar = 1.00 # um valor qualquer para pagar
                padaria.FP1.append(cliente)
                # gerar a saida desse cara da fila 2
                eventosa = Evento(1, ungeraexp(1/85, vetuni3[0])+le[0].tempo, 2)
                eventosa.setacheg(le[0].tempo)
                vetuni3.remove(vetuni3[0])
                le.append(eventosa)
             elif(padaria.pessoasemfila(2) >= K):

                print("desistiu") # ou descarte da fila 2
                ED = ED+1 # "calote" (descarte da fila 2)

             EK1 += padaria.pessoasemfila(1)
             EK2 += padaria.pessoasemfila(2)
             le.remove(le[0])  # removendo o evento atual
             le.sort(key=lambda evento: evento.tempo)
            # if (len(le) > 0):
             mins = le[0].tempo # pega o proximo



          #   print("minutos: ", mins)

        elif (le[0].tipo == 1 and le[0].fila == 2 and le[0].tempo == mins):
            EWi2 += le[0].tempo - le[0].cheg  # (saida - chegada) (intervalo efetivo)
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

            EK1 += padaria.pessoasemfila(1)
            EK2 += padaria.pessoasemfila(2)
            le.remove(le[0])  # removendo o evento atual
            le.sort(key=lambda evento: evento.tempo)
            if(len(le) > 0 ):
                mins = le[0].tempo


           # print("minutos: ", mins)

    elif(len(le)==0):
            mins = tempomax # nao tem evento na lista
            print(mins)
        # print("minutos: ", mins)
