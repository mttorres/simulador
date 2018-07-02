import math
import time
from evento.evento import Evento

###### para varios valores########
#gerador  n valores uniformes
def conglinear(a,c,m,x,vet,n):
    for i in range(0,n):
        xp = ((x*a) +c)%m
        u = xp/m
        vet.append(u)
        x = xp


# gerador exeponencial usando os valores uniformes
def geraexp(lamb,vetuni):
    vetexp = []
    for x in vetuni:
        res = (-(math.log(1-x)))/lamb
        vetexp.append(res)
    return vetexp


# arredondar CASO NECESSARIO
def geraexpdiscret(vetexp):
    for i in range(0,len(vetexp)):
        vetexp[i] = round(vetexp[i]) # evita(cieling) que alguns caras cheguem no tempo zero ...




##### para um valor#####


def unconglinear(a,c,m,s):
    if(s != 0):
        x = ((s*a) + c)%m
        u = x / m
    else:
        x = (time.time()* a + c) % m
        u = x/ m
    return u

def ungeraexp(lamb,u):
    #x =unconglinear(13445,0,2**31-1,s)  # ex: antede um cliente a cada 3 minutos: rate = 1/3 a formula é ln(1-x)/1/lamb que é a mesma coisa que multiplicar
    res = (-(math.log(1 - u))) / lamb  # ex: 1/40 1 terremoto a cada 40 mins em algum lugar do mundo
    return res








''' TESTES
def geradoreventos(vet,tipo,tempo):
    evento = Evento(tipo, vet[0]+tempo)
    vet.remove(vet[0])
    return evento
'''

''''''
vetuni = []
vetuni2 =[]
vetuni3 = []
#s = 5
#qtd = 33000
conglinear(13445,0,2**31-1,5000,vetuni,3600000//110) # testando com qtd numeros e semente USAR DIFERENTES SEMENTES!
vetuni.sort()
#conglinear(13445,0,2**31-1,s,vetuni2,40000)
#conglinear(13445,0,2**31-1,s,vetuni2,40000)
expat = geraexp(1/110,vetuni) # tempos de chegada da fila atendimento
#exppa = geraexp(1/90,vetuni) # tempos de saida da fila de atendimento e entrada da fila pagamento
#expat.sort()
print(max(vetuni))
print(ungeraexp(1/110,vetuni[0]))
print(expat)

'''


'''
vet = []
conglinear(13445,0,2**31-1,5,vet,1000)
vetexp = geraexp(1/110,vet) 
c = 0
for x in vetexp:
    c = c + x

media = c/1000
print(media) # como esperado proxima de 90!
geraexpdiscret(vetexp)
print(vetexp)
'''

#def geradoreventos()

# com essas funções temos EXATAMENTE o tempo que ocorre cada evento!
# duvida... devemos deixar esses numeros discretos? (pode atrapalhar a simulação se formos contar cada centesimo e segundo... vai ficar mt longa!)
# porem se deixar discreta com numeros inteiros poderiamos ter valores desiguais de numeros??
   #outra função para testar :


# NAO UTILIZADO (TESTES)######
#print("VETOR NUMEROS UNIFORME: ")
#print()
#print(vet)
#print()
'''
c= 0

for x in vetexp:
    c = c + x

media = c/1000
print(media) # como esperado proxima de 40!

vetexp = geraexp(1,vet)

for x in vet:
    if x > 1:
        print("AAAAAAAAAAA")


c = 0
for x in vetexp:
    if x > 1:
        c += 1
        print("BBBBBBBBB",c)
        


#print(vetexp)'''
'''
Distribuição exponencial prorpiedade MEMORYLESS:
    a chance de algo acontecer em um periodo de t unidades de tempo ainda é a mesma
    ex:
        P[t >40 | t>30] = p[t >10] nao importa quanto tempo passou antes somente os t segundos! (independencia)
        eventos nao ocorrem exatamente no mesmo instante
        a taxa a qual os eventos ocorrem é constante (lambda)
        a probabilidade de um evento ocorrer nao afeta a probabilidade de um segundo evento (independencia)
    
Distribuição Poisson
#S tempo entre as chegadas
# poisson  eventos de chegada quantos eventos(K) aconteceram em t

pode usar exponencial para simular, 
#P[S > t]


'''