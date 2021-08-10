# -*- coding: UTF-8 -*-
import math

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
        Spinor[i][0]=Spinor[i][1]
        Spinor[i][1]=-1*a
    return Spinor