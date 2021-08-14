# -*- coding: UTF-8 -*-
import math
import cmath

#Initialize of the beam
def Initialize(InitialPolarizationDegree,ParticleNum):
    print 'Initializing...'
    print('InitialPolarizationDegree ' ,InitialPolarizationDegree)
    print('particlenum ' ,ParticleNum)
#A simples‘t initialization for test (21-8-10)

#for a polarization degree P beam ,assume all electrons are spin up or spin down ,
#the number of spin up  electrons is N* (P+1)/2, in this case assume spinupNum is integer
    SpinUpNum=((InitialPolarizationDegree+1)/2)*ParticleNum
    Spinor=[]
    for i in range(ParticleNum):
            if i < SpinUpNum:
                Spinor.append([complex(1),complex(0)])
            else:
                Spinor.append([complex(0),complex(1)])

    print 'Initialization done'

    return Spinor

#Arc with angle 2pi,without any resonance
#Arc that do not change the spinor in memory,only return a spinor
def Arc(Spinor,GGamma):
    Length=len(Spinor)
    SpinorInM=[]
    for i in range(Length):
        SpinorU=Spinor[i][0]*(math.cos(GGamma*math.pi)-math.sin(GGamma*math.pi)*1j)
        SpinorD=Spinor[i][1]*(math.cos(GGamma*math.pi)+math.sin(GGamma*math.pi)*1j)
        #SpinorInM[i][0]=Spinor[i][0]*(math.cos(GGamma*math.pi)-math.sin(GGamma*math.pi)*1j)
        #SpinorInM[i][1]=Spinor[i][1]*(math.cos(GGamma*math.pi)+math.sin(GGamma*math.pi)*1j)
        SpinorInM.append([SpinorU,SpinorD])
    return SpinorInM

#A full snake with angle pi,snake axis lies on the beam direction.
#def Snake(Spinor):
 #   Length=len(Spinor)
  #  for i in range(Length):
   #     a=Spinor[i][0]
   #     Spinor[i][0]=-1*Spinor[i][1]
    #    Spinor[i][1]=a
   # return Spinor

#A full snake with angle pi,snake axis on transverse radial direction.
#def Snake2(Spinor):
  #  Length=len(Spinor)
   # for i in range(Length):
   #     a=Spinor[i][0]
   #     Spinor[i][0]=-1j*Spinor[i][1]
   #     Spinor[i][1]=-1j*a
    #return Spinor


#A general snake module
#the snake axis direction is (cos[phis] ,sin[phis] , 0)
#phis varies from -pi to pi,phi from 0 to pi.
def Snake(Spinor,phi,phis):
    cc=math.cos((phi/2)*math.cos(phis))
    cs=math.cos((phi/2)*math.sin(phis))
    ss=math.sin((phi/2)*math.sin(phis))
    sc=math.sin((phi/2)*math.cos(phis))
    m11=cc*cs-1j*ss*sc
    m12=-1*cc*ss-1j*cs*sc
    m21=cc*ss-1j*cs*sc
    m22=cc*cs+1j*ss*sc

    Length=len(Spinor)
    for i in range(Length):
        a=Spinor[i][0]
        Spinor[i][0]=m11*Spinor[i][0]+m12*Spinor[i][1]
        Spinor[i][1]=a*m21+m22*Spinor[i][1]

    #return Spinor
    return
  



#rotate into resonance precessing frame ,apply the resonance kick then rotate back to particle rest frame
####(the strength of resonance is replaced by a estimated value of 0.002*GGamma )####deleted####
#eplison is the strength of resonance ,it is a complex
#The calculation is based on the Spin Transfer Matrix of constant GGamma ,suitable for all kinds of resonance
#The resonance kick is applied in a complete turn ie. theta from 0 to 2pi
def ResonanceKick(Spinor,GGamma,K,eplison):
    #eplison=GGamma*0.002
    delta=K-GGamma
    lamda=math.sqrt(delta*delta+abs(eplison)*abs(eplison))
    b=(abs(eplison)*math.sin(lamda*math.pi))/lamda
    a=math.sqrt(1-b*b)

    if (lamda-int(lamda)>0.5):       #Fix the error that arctan(Tan(x)) may lost some phase of a (integer*pi)
        AngleNum=int(lamda+1)
    else:
        AngleNum=int(lamda)

    c=math.atan((delta*math.tan(lamda*math.pi))/lamda)+AngleNum*math.pi
    d=-1*cmath.phase(eplison)
    
    Length=len(Spinor)
    for i in range(Length):
        
        x=Spinor[i][0]
        Spinor[i][0]=Spinor[i][0]*a*cmath.exp((c-K*math.pi)*1j)+1j*b*Spinor[i][1]*cmath.exp(-1j*(d+K*math.pi))
        Spinor[i][1]=x*(1j)*b*cmath.exp(1j*(d+K*math.pi))+Spinor[i][1]*a*cmath.exp(-1j*(c-K*math.pi))
       

    return
    #return Spinor




#Calculate polarization degree
#polarization degree=<<Sigma3>>
def CalPorDegree(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        sigmai=abs(Spinor[i][0])*abs(Spinor[i][0])-abs(Spinor[i][1])*abs(Spinor[i][1])
        sigma.append(sigmai)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/Length
    #print(sigma)

    return Pordegree


#To calculate the modules of Spinors 
def CalModules(Spinor):
    Length=len(Spinor)
    module=[]
    for i in range(Length):
        Module=abs(Spinor[i][0])*abs(Spinor[i][0])+abs(Spinor[i][1])*abs(Spinor[i][1])
        module.append(Module)
    
    return module

