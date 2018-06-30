conglinear <- function(a,c,m,x,vetor)
{
  
  if(length(vetor) == 1000)
  {
    return(vetor)  
  }
  else
  {
    y <- ((x*a)+c)%%m
    u <- y/m 
    vetor<- c(vetor,u)
    conglinear(a,c,m,y,vetor)
  }
  
  
}

# parametros: # IN
#vet = conglinear(13445,0,2**31-1,5,vet) # PARAMETROS DA BIBLIOTECA DE R, seed 5
#vet3 = conglinear(13445,0,2**31-1,7,vet3) # seee 7
#vet2 = conglinear(13445,0,2**31-1,32,vet) # seed 32

# OUT 
vetout = conglinear(13445,0,2**31-1,10,vetout)
vetout2 = conglinear(13445,0,2**31-1,14,vetout2)
vetout3 = conglinear(13445,0,2**31-1,64,vetout3)
# OUT 2

#...

vetin = geraexp(5,vet)
vetin2 = geraexp(2,vet)
vetin3 = geraexp(1,vet)

geraexp <- function(lamb,vetuni)
{
  vetexp <- c()
  for (x in vetuni) 
  {
    res <- (-lamb*log(1-x))  
    vetexp <- c(vetexp,res)
  }
  return (vetexp)
  
  
}

# vizualização
hist(vetin, 
     main="Gerando Distribuição Exponencial parametros : \n  lambda = 5", 
     xlab="Números",
     ylab = "Frequência",
     xlim=c(0,45),
     ylim=c(0,400),
     las=1, 
     breaks=20)

hist(vetin, 
     main="Gerando Distribuição Exponencial parametros : \n  lambda = 5", 
     xlab="Números",
     ylab = "Frequência",
     xlim=c(0,100),
     ylim=c(0,400),
     las=1, 
     breaks=20)



hist(vetin2, 
     main="Gerando Distribuição Exponencial parametros : \n  lambda = 2", 
     xlab="Números",
     ylab = "Frequência",
     xlim=c(0,45),
     ylim=c(0,400),
     las=1, 
     breaks=20)



hist(vetin2, 
     main="Gerando Distribuição Exponencial parametros : \n  lambda = 2", 
     xlab="Números",
     ylab = "Frequência",
     xlim=c(0,30),
     ylim=c(0,500),
     las=1, 
     breaks=20)


hist(vetin3, 
     main="Gerando Distribuição Exponencial parametros : \n  lambda = 2", 
     xlab="Números",
     ylab = "Frequência",
     xlim=c(0,45),
     ylim=c(0,400),
     las=1, 
     breaks=20)




hist(vetin3, 
     main="Gerando Distribuição Exponencial parametros : \n  lambda = 2", 
     xlab="Números",
     ylab = "Frequência",
     xlim=c(0,15),
     ylim=c(0,500),
     las=1, 
     breaks=20)

