import random

class Ant:
   
    PosDispo=[]
    Caminho=[]

    def __init__(self,origem,objetivo):
        self.posJ=origem[0]
        self.posI=origem[1]
        self.ObjetivoJ=objetivo[0]
        self.ObjetivoI=objetivo[1]

    def reeset(self,origem):
        self.posJ=origem[0]
        self.posI=origem[1]
        self.PosDispo.clear()
        self.Caminho.clear()
        
    def andar(self,proximo):
        self.posJ=proximo[0]
        self.posI=proximo[1]
        self.Caminho.append([self.posJ,self.posI])
        self.PosDispo.clear()
           

    def find(self):
        if((self.posI == self.ObjetivoI) and (self.posJ == self.ObjetivoJ)):
            self.Caminho.append([self.posJ,self.posI])
            return True 
        else:
            return False
         
    def caminhoLivre(self,matrix):
        if(matrix.PathMatrix[self.posI][self.posJ+1]==0 or matrix.PathMatrix[self.posI][self.posJ+1]==3):
            self.PosDispo.append([self.posJ+1,self.posI])

        if(matrix.PathMatrix[self.posI][self.posJ-1]==0 or matrix.PathMatrix[self.posI][self.posJ-1]==3):
            self.PosDispo.append([self.posJ-1,self.posI])

        if(matrix.PathMatrix[self.posI+1][self.posJ]==0 or  matrix.PathMatrix[self.posI+1][self.posJ]==3):
            self.PosDispo.append([self.posJ,self.posI+1])

        if(matrix.PathMatrix[self.posI-1][self.posJ]==0 or matrix.PathMatrix[self.posI-1][self.posJ]==3):
            self.PosDispo.append([self.posJ,self.posI-1])
            
        if( [self.ObjetivoJ,self.ObjetivoI] in self.PosDispo):
            self.PosDispo.clear()
            self.posI=self.ObjetivoI
            self.posJ=self.ObjetivoJ
            return

    def fechado(self):
        if (len(self.PosDispo)==0 and (not self.find())):
            return True
        else: 
            return False
                
    def choose(self,mapa):
        if(not self.find()):
            if(len(self.PosDispo)==1):
                self.andar(self.PosDispo[0])
            else:
                feromonios=[]
                sum=0
                for pnt in self.PosDispo:
                    feromonios.append(mapa.FeromonMatrix[pnt[1]][pnt[0]])
                    sum+=mapa.FeromonMatrix[pnt[1]][pnt[0]]

                val=random.randint(0,int(sum))
                intervalo1=int(feromonios[0])
                intervalo2=int(feromonios[1]) + int(feromonios[0])
                
                if(val in range(1,intervalo1)):
                    self.andar(self.PosDispo[0])
        
                elif(val in range(intervalo1, intervalo2 + 1 ) ):
                    self.andar(self.PosDispo[1])
                else:
                    self.andar(self.PosDispo[-1])



    

class Labrinth:
    
    PathMatrix=[]
    FeromonMatrix=[]
    pnt_init=[]
    pnt_end=[]
    FeromRate=0.3
    EvapoRate=0.4
    
    def __init__(self,file):
        f = open(file,'r') 
        f_content = f.readlines()
        matrix1=[]
        matrix2=[]
        matrix3=[]

        for i in f_content:
            for  j in i:    
                if(j==' '):
                    matrix2.append(0)
                elif(j=='S'):
                    matrix2.append(2)
                elif(j=='E'):
                    matrix2.append(3)
                else:
                    matrix2.append(1)
            aux=matrix2.copy()
            matrix1.append(aux)
            matrix2.clear()
        
        f.close()
        

        for line in matrix1:
            for i in range(0,len(line),2):
                matrix2.append(line[i])
            aux=matrix2.copy()
            matrix3.append(aux)
            matrix2.clear()
        
        self.PathMatrix=matrix3.copy()
        matrix3.clear()

         
        for i in self.PathMatrix:
            if (2 in i):
                    self.pnt_init.append(i.index(2)) 
                    self.pnt_init.append(self.PathMatrix.index(i)) 
            if (3 in i):
                    self.pnt_end.append(i.index(3))
                    self.pnt_end.append(self.PathMatrix.index(i)) 
            for j in i:
                if(j==1):
                    matrix2.append(0)
                else:
                    matrix2.append(random.random()*100)
            aux=matrix2.copy()
            self.FeromonMatrix.append(aux)
            matrix2.clear()

    def Atualizapath(self,Formiga):
            posI=Formiga.Caminho[-1][1]
            posJ=Formiga.Caminho[-1][0]
            self.PathMatrix[posI][posJ]=4
    
    def CleanTrail(self,Formiga):
         for pnt in Formiga.Caminho:
            if( self.PathMatrix[pnt[1]][pnt[0]] == 4 ):
                self.PathMatrix[pnt[1]][pnt[0]] = 0 

    def AtualizaFerom(self,Formiga):
        for l in self.FeromonMatrix:
            for j in range(len(l)):
                if (l[j] > 0):
                    l[j]=l[j]*(1-self.EvapoRate)
        
        for pnt in Formiga.Caminho:
            self.FeromonMatrix[pnt[1]][pnt[0]]= self.FeromonMatrix[pnt[1]][pnt[0]]*(1.0+self.FeromRate)

    def print(self):
        cont=0
        print (" ")
        for j in  range(len(self.PathMatrix)):
            print(j,end=" ")
        for i in self.PathMatrix:
            print(cont,end=" "),print(i)
            cont +=1 
            

            

                        
    
        
              
        
#Inicio do programa

mapa = Labrinth("LabirintoExemplo01.txt")
Colonia=[]
NC=30

for i in range(10):
    ant=Ant(mapa.pnt_init,mapa.pnt_end)
    Colonia.append(ant)
    del ant
  

for m in range(len(Colonia)):
    Colonia[i].caminhoLivre(mapa)
    while(not Colonia[i].find()):
        Colonia[i].choose(mapa)
        mapa.Atualizapath(Colonia[i])
        Colonia[i].caminhoLivre(mapa)
        if (Colonia[i].fechado()):
            mapa.CleanTrail(Colonia[i])
            Colonia[i].reeset(mapa.pnt_init)
            Colonia[i].caminhoLivre(mapa)
    mapa.AtualizaFerom(Colonia[i])
    mapa.CleanTrail(Colonia[i])
    Colonia[i].reeset(mapa.pnt_init)
    Colonia[i].caminhoLivre(mapa)



#for i in range(50):
#        Colonia.append(Ant(mapa.pnt_init,mapa.pnt_end))
#
#for m in range(NC):
#    
#        Colonia[i].caminhoLivre(mapa)
#        while(not Colonia[i].find()):
#            Colonia[i].choose(mapa)
#            mapa.Atualizapath(Colonia[i])
#            Colonia[i].caminhoLivre(mapa)
#            if (Colonia[i].fechado()):
#                Colonia[i].reeset()
#                mapa.CleanTrail()
#        if(Colonia[i].find()):
#            mapa.AtualizaFerom(Colonia[i])
#        mapa.CleanTrail(Colonia[i])

    
   

#    Colonia[0].caminhoLivre(mapa)
#    Colonia[0].choose(mapa)
#    mapa.Atualizapath(Colonia[0])
#
#    Colonia[0].caminhoLivre(mapa)
#    Colonia[0].choose(mapa)
#    mapa.Atualizapath(Colonia[0])
#
#    Colonia[0].caminhoLivre(mapa)
#    Colonia[0].choose(mapa)
#    mapa.Atualizapath(Colonia[0])
#
#    Colonia[0].caminhoLivre(mapa)
#    Colonia[0].choose(mapa)
#    mapa.Atualizapath(Colonia[0])
#
#    Colonia[0].caminhoLivre(mapa)
#    Colonia[0].choose(mapa)
#    mapa.Atualizapath(Colonia[0])
#
#    Colonia[0].caminhoLivre(mapa)
#    Colonia[0].choose(mapa)
#    mapa.Atualizapath(Colonia[0])
#
#
#
#    mapa.AtualizaFerom(Colonia[0])
#
#    mapa.CleanTrail(Colonia[0])
#
#print("Fim")
#for k in Colonia:
    #k.caminhoLivre(mapa.PathMatrix)
    #while(not(k.PosDispo.empty() or k.find())):


        


            


    
        