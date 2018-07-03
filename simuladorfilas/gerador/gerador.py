import math
import time

#       para varios valores         #
#       gerador  n valores uniformes#
def conglinear(a,c,m,x,vet,n):
    for i in range(0, n):
        xp = ((x*a) + c) % m
        u = xp/m
        vet.append(u)
        x = xp


# gerador exeponencial usando os valores uniformes
def geraexp(lamb, vetuni):
    vetexp = []
    for x in vetuni:
        res = (-(math.log(1-x)))/lamb
        vetexp.append(res)
    return vetexp


# arredondar CASO NECESSARIO
def geraexpdiscret(vetexp):
    for i in range(0, len(vetexp)):
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
    res = (-(math.log(1 - u))) / lamb  # ex: 1/40 1 terremoto a cada 40 mins em algum lugar do mundo
    return res





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