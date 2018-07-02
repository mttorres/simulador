from padaria.cliente import Cliente
from padaria.padaria import Padaria
from evento.evento import Evento
from gerador.gerador import conglinear, geraexp, unconglinear, geraexpdiscret,ungeraexp
import time
# OBS'S: criar uma classe padaria? que guarda informações relevantes tipo o lucro total... etc ou as filas?
#estados: definido pelo N das filas
# eventos: CHEGADA,SAIDA,DESISTIU(?), DE UMA FILA EM UM CERTO TEMPO
#todo: FAZER UMA ENTRADA QUE ESCOLHA O VALOR DE EC!
# parametros:
# ambos sao exponenciais, valores esperado de uma variavel com distribuição exponencial = 1/lambda
# o a fila 1 chegada a cada 110ms , lambda= 1/110 e tem processamento 90 ms, fazendo a fila 2 ter chegada 1/90
EX = 90 #  lembrando que ele quer que usemos E[X] = 90 ms como parametro (tempo medio para servir uma requisição)(lambda = 1/90 é aproximadamente 11 se a unidade for segundos)
EC = 110 # lembrando que ele quer quer que usemos E[C] = 110 ms como parametro(intervalo de tempo medio entre chegadas(lambda= 1/100 é aproximadamente 9 se a unidade for segundos)

tempomax = 3600000 # 60 MINUTOS tempo de simulação (nao é realmente necessário ser tempo real)
# como EC pode mudar (de acordo com o enunciado do trabalho)(diferentes experimentos) seria interessante deixar generico
# e o EC ser definido por entrada!
# VETORES DE NUMEROS ALEATORIOS ENTRE 0 E 1
vetuni = [] # vetor unitario com x numeros entre 0 e 1 # ~32 mil numeros (chegada fila 1)(lamb / 110)
conglinear(13445,0,2**31-1,5000,vetuni,tempomax//EC)
vetuni.sort() # ordenados...
vetuni2 =[] # 40 mil numeros (saida fila 1) e chegada fila 2 (usa semente maior para fazer as saidas tenderem a serem maior que as chegadas)
conglinear(13445,0,2**31-1,15000,vetuni2,tempomax//EX)
vetuni2.sort()
vetuni3 = [] # ~42 mil numeros (saida fila 2)
conglinear(13445,0,2**31-1,20000,vetuni3,tempomax//85)
vetuni3.sort()

#medidas de interesse
EWi1 = 0 # tempo medio que uma requisição permanece no sistema (somar o tempo de permanencia(saida - chegada) de todos)(fila1)
EWi2 = 0 #
EWt = 0 # EWt1 + probdesistenciaxEWt2
ED = 0 # taxa de descarte (desistencias)?
EDD = 0 # taxa de descarte mesmo K == 15?
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
le.append(evento0) # eventos SAO ORDENADAOS POR ORDEM DE OCORRENCIA!
# contador minutos(loop da simulação)
timeLoop = True
#mins = 0    # por quanto tempo devemos por ja que ele botou mili segundos!?
mins = 0 # tempo decorrido ate agora
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
    #print("minutos: ",mins)
    if (mins == tempomax):
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

        break
    #time.sleep(1)
    if (len(le) > 0 ): # tem evento para acontecer
        if (le[0].tipo == 0 and (mins <= le[0].tempo <= mins+1)):  # é um evento de chegada
            print("cheguei!")
            print("tempo",le[0].tempo)
            c = Cliente()
            if (padaria.pessoasemfila(1) < K):
                N += 1
                NC+= 1
                padaria.FA1.append(c) # jogou na fila 1
                #gerar proxima chegada(outro cara) e a saida desse que chegou agora(que é tmb a chegada na fila 2)
                eventoch = Evento(0, ungeraexp(1 / EC, vetuni[0]), 1)
                eventosa = Evento(1, ungeraexp(1 / EX, vetuni2[0])+le[0].tempo, 1) # salva o tempo de saida(chegada + o tempo gerado)
                eventosa.setacheg(le[0].tempo) # salva o tempo de chegada e temos agora o intervalo (saida - chegada)
                vetuni.remove(vetuni[0]) # remove da lista de valores 0,1 para nao ter repetições
                vetuni2.remove(vetuni2[0])
                le.append(eventoch)
                le.append(eventosa)
                # e adicionar a lista de eventos
                le.sort(key = lambda evento: evento.tempo) # ordenada a lista de eventos
            else:
                print("descarte")
                EDD = EDD + 1 # contando os descartes e dps fazer a media no final do programa EDD/total de chegadas
            #independente do descarte ou nao a chegada aconteceu e deve ser removida da lista e o tempo mins atualizado
            mins += le[0].tempo
            le.remove(le[0])  # removendo o evento atual
         #   print("minutos: ", mins)
                                                                                                    # esse evento acontece efetivamente após chegada + saida
        elif(le[0].tipo == 1 and le[0].fila == 1 and (mins <= le[0].tempo <= mins+1)): # evento de saida da fila 1 (e chegada na fila2)
             print("saida fila 1!")
             #N-= 1 NA VDD ELE CONTINUA NO SISTEMA
             NS+=1 # saida da fila 1
             EWi1 += le[0].tempo - le[0].cheg # (saida - chegada) (intervalo efetivo) de cada elemento na fila 1
             padaria.deveriareceber += 9.50 # deveria receber um valor de +9.50$
             if (padaria.pessoasemfila(2) < K and padaria.pessoasemfila(1) > 0):
                # processar o evento de saida da fila 1!
                NC2 += 1
                cliente = padaria.FA1.popleft() # devolve o cara que saiu dessa fila... # e que deve entrar na segunda fila!
                cliente.a_pagar = 9.50 # um valor qualquer para pagar
                padaria.FP1.append(cliente)
                # gerar a saida desse cara da fila 2
                eventosa = Evento(1, ungeraexp(1/85, vetuni3[0])+le[0].tempo, 2)
                eventosa.setacheg(le[0].tempo)
                vetuni3.remove(vetuni3[0])
                le.append(eventosa)
                le.sort(key=lambda evento: evento.tempo)
             else:
                print("desistiu") # ou descarte da fila 2
                #EDD = EDD+1 # descarte
                ED = ED+1 # "calote" PREJUIZO!(descarte da fila 2)

             mins += le[0].tempo - le[0].cheg # atualiza o minuto com o intervalo de tempo até o evento de processamento e mudança de fila acontecer efetivamente
             le.remove(le[0])  # removendo o evento atual
          #   print("minutos: ", mins)

        elif (le[0].tipo == 1 and le[0].fila == 2 and (mins <= le[0].tempo <= mins+1)):
            EWi2 += le[0].tempo - le[0].cheg  # (saida - chegada) (intervalo efetivo)
            if (padaria.pessoasemfila(2)  > 0):
                print("saida fila 2!( e da padaria)")
                N -= 1 # 1 saida do sistema (total de pessoas no sistema diminui)
                NS2+= 1 # uma saida da fila 2
                NSS+= 1 # adiciona uma saida do sistema
                cliente = padaria.FA1.popleft()
                padaria.recebeu += cliente.a_pagar  # padaria recebeu + 9.50
            else:
                print("isso nao deveria acontecer")
                print("ele nao deveria tentar remover alguem da fila 2 sem ter ninguem!?")
            mins += le[0].tempo - le[0].cheg
            le.remove(le[0])  # removendo o evento atual
           # print("minutos: ", mins)

        else:
            mins = mins+1 # nao tem evento na lista
           # print("minutos: ", mins)

<<<<<<< HEAD
# OBS pf observem se eu nao esqueci de atualizar algum valor de interesse no loop...
=======
    if mins == tempomax:  # teste....
        print("Simulação terminada")
       # print(padaria.FA1)  # seria interessante criar um metodo str para o cliente para o print nao ficar feio kkk e facilitar debugar
       # print(padaria.FA2)
        print(le)  # tem que terminar vazia
        break
>>>>>>> 283342a022db6759d43e9031081f82c639ff3927
