import math

#gerador uniforme
def conglinear(a,c,m,x,vet):
    for i in range(0,999):
        xp = ((x*a) +c)%m
        u = xp/m
        vet.append(u)
        x = xp


# gerador exeponencial

def geraexp(lamb,vetuni):
    vetexp = []
    for x in vetuni:
        res = (-lamb*(math.log(1-x)))
        vetexp.append(res)
    return vetexp


vet = []
conglinear(13445,0,2**31-1,5,vet)


#todo 
#def geradoreventos()



#print("VETOR NUMEROS UNIFORME: ")
#print()
#print(vet)
#print()
'''
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