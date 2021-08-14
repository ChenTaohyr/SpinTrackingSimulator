#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import source
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
import math
      
file_name = sys.argv[1]           #Get input file

f=open(file_name)
parameters={}
while True:                      #Read every parameters and save them in dir 
         line=f.readline()
         line=line.strip()
         if not line:
              break
         else:
             parameters[line.split('=')[0]] = line.split('=')[1] 
             
             
f.close()   
    
print('parameters: ' ,parameters)

#initialize the beam
Spinor=\
source.Initialize(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))

#read resonance data
ResonanceFile=parameters['ResonanceFile']
#print(ResonanceFile,type(ResonanceFile))

f=open(ResonanceFile)
ResonanceData={}
while True:                      
         line=f.readline()
         line=line.strip()
         if not line:
              break
         else:
              ResonanceStrength=float(line.split(' ')[1])+1j*float(line.split(' ')[2])   #Read and save resonance strength as complex
              print(ResonanceStrength)
              ResonanceData[float(line.split(' ')[0])] =ResonanceStrength
             
             
f.close() 


#SpinorAfterArc=source.Arc(Spinor,GGamma)
#Spinor2=source.Snake(SpinorAfterArc)

G=0.001159652

#For picture
#PorPlotY=[]
#PorPlotX=[]


####deleted####
#electron energy from 0 to 40GeV,corresponding to Gamma from 1 to 80000
#Gamma raise 1 per turn
#Temporarily，only regular imperfection resonances is considered
#Resonance tune K is selected as the integer nearest GGamma


#for i in range(1):
#     Gamma=i+100
 #    GGamma=G*Gamma
 #   IntGGamma=int(GGamma)
  #   if (GGamma-IntGGamma>0.5):
   #       K=IntGGamma+1
    #      SpinorAfterKick=source.ResonanceKick(Spinor,GGamma,K,0)
     #     Spinor=source.Snake(SpinorAfterKick,pi,0)
      #    if(i%100==1):
       #        p=source.CalPorDegree(Spinor)
        #       #p=source.CalPorDegree(SpinorAfterKick)
         #      PorPlotX.append(GGamma)
          #     PorPlotY.append(p)
     #else:
     #     K=IntGGamma
     #    SpinorAfterKick=source.ResonanceKick(Spinor,GGamma,K,0)
     #     Spinor=source.Snake(SpinorAfterKick,pi,0)
     #     if(i%100==1):
     #          p=source.CalPorDegree(Spinor)
     #          #p=source.CalPorDegree(SpinorAfterKick)
     #          PorPlotX.append(GGamma)
     #          PorPlotY.append(p)
#####


#Implement the acceleration
###deleted###Temporarily, only resonance that close to GGamma is considered###
InitialGamma=int(parameters['InitialGamma'])
FinalGamma=int(parameters['FinalGamma'])
EnergyRisePerTurn=float(parameters['EnergyRisePerTurn'])
Gamma=InitialGamma

'''
#for Test , only Arc is implemented to the particle
Gamma2=InitialGamma

while (Gamma2<FinalGamma):
          GGamma=G*Gamma2
          SpinorTest=source.Arc(Spinor,GGamma)
          Gamma2=Gamma2+EnergyRisePerTurn

print(Spinor)
print('final spinor_Arc', SpinorTest)
print('Modules of the spinors_Arc', source.CalModules(SpinorTest))
p2=source.CalPorDegree(SpinorTest)
print('final polarization degree_Arc',p2)

'''

#ResonanceNum=len(ResonanceData)
#print(ResonanceNum)
while (Gamma<FinalGamma):
          GGamma=G*Gamma

          for i in ResonanceData:
               #if(abs(GGamma-i)<=0.5 ):
                    #Spinor=source.ResonanceKick(Spinor,GGamma,i,complex(GGamma*ResonanceData[i]))
                    source.ResonanceKick(Spinor,GGamma,i,complex(ResonanceData[i]))  #Resonance Strength not rely on GGamma


          if (parameters['UseSnake']=='1'):
               source.Snake(Spinor,float(parameters['phi']),float(parameters['phis']))

          Gamma=Gamma+EnergyRisePerTurn
print('final spinor', Spinor)
print('Modules of the spinors', source.CalModules(Spinor))
p=source.CalPorDegree(Spinor)
print('final polarization degree',p)
alpha=G*EnergyRisePerTurn/(2*math.pi)
_4piq=math.pi*abs(ResonanceStrength)*abs(ResonanceStrength)/(2*alpha)
print('4piq',_4piq)





#Draw the picture of the change of porlization degree
#print(PorPlotX)
#print(PorPlotY)
#plt.scatter(PorPlotX, PorPlotY)
#plt.show()