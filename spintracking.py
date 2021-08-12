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
             ResonanceData[float(line.split(' ')[0])] = float(line.split(' ')[1] )
             
             
f.close() 
#print(ResonanceData)

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
#Temporarily, only resonance that close to GGamma is considered
InitialGamma=int(parameters['InitialGamma'])
FinalGamma=int(parameters['FinalGamma'])
EnergyRisePerTurn=int(parameters['EnergyRisePerTurn'])
Gamma=InitialGamma
#ResonanceNum=len(ResonanceData)
#print(ResonanceNum)
while (Gamma<FinalGamma):
          GGamma=G*Gamma

          for i in ResonanceData:
               if(abs(GGamma-i)<=0.5 ):
                    Spinor=source.ResonanceKick(Spinor,GGamma,i,complex(GGamma*ResonanceData[i]))

          if (parameters['UseSnake']=='1'):
               Spinor=source.Snake(Spinor,float(parameters['phi']),float(parameters['phis']))
          Gamma=Gamma+EnergyRisePerTurn

p=source.CalPorDegree(Spinor)
print(p)





#Draw the picture of the change of porlization degree
#print(PorPlotX)
#print(PorPlotY)
#plt.scatter(PorPlotX, PorPlotY)
#plt.show()




