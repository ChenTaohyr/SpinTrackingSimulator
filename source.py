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
def Arc(Spinor,GGamma):
    Length=len(Spinor)
    for i in range(Length):
        Spinor[i][0]=Spinor[i][0]*(math.cos(GGamma*math.pi)-math.sin(GGamma*math.pi)*1j)
        Spinor[i][1]=Spinor[i][1]*(math.cos(GGamma*math.pi)+math.sin(GGamma*math.pi)*1j)
    return Spinor

#A full snake with angle pi,snake axis lies on the beam direction.
def Snake(Spinor):
    Length=len(Spinor)
    for i in range(Length):
        a=Spinor[i][0]
        Spinor[i][0]=-1*Spinor[i][1]
        Spinor[i][1]=a
    return Spinor

#A full snake with angle pi,snake axis on transverse radial direction.
def Snake2(Spinor):
    Length=len(Spinor)
    for i in range(Length):
        a=Spinor[i][0]
        Spinor[i][0]=-1j*Spinor[i][1]
        Spinor[i][1]=-1j*a
    return Spinor

#rotate into resonance precessing frame ,apply the resonance kick then rotate back to particle rest frame
#the strength of resonance is replaced by a estimated value of 0.002*GGamma 
def ResonanceKick(Spinor,GGamma,K):
    eplison=GGamma*0.002
    delta=K-GGamma
    lamda=math.sqrt(delta*delta+eplison*eplison)
    b=(eplison*math.sin(lamda*math.pi))/lamda
    a=math.sqrt(1-b*b)
    c=math.atan((delta*math.tan(lamda*math.pi)/lamda))
    d=0
    
    Length=len(Spinor)
    for i in range(Length):
        
        x=Spinor[i][0]
        Spinor[i][0]=Spinor[i][0]*a*cmath.exp((c-K*math.pi)*1j)+1j*b*Spinor[i][1]*cmath.exp(-1j*(d+K*math.pi))
        Spinor[i][1]=x*(-1j)*b*cmath.exp(1j*(d+K*math.pi))+Spinor[i][1]*a*cmath.exp(-1j*(c-K*math.pi))
       


    return Spinor




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


