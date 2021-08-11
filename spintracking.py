#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import source
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
      
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

Spinor=\
source.Initialize(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))


#SpinorAfterArc=source.Arc(Spinor,GGamma)
#Spinor2=source.Snake(SpinorAfterArc)

G=0.001159652

#For picture
PorPlotY=[]
PorPlotX=[]

#electron energy from 0 to 40GeV,corresponding to Gamma from 1 to 80000
#Gamma raise 1 per turn
#Temporarily，only regular imperfection resonances is considered
#Resonance tune K is selected as the integer nearest GGamma


for i in range(8000):
     Gamma=i+100
     GGamma=G*Gamma
     IntGGamma=int(GGamma)
     if (GGamma-IntGGamma>0.5):
          K=IntGGamma+1
          SpinorAfterKick=source.ResonanceKick(Spinor,GGamma,K)
          Spinor=source.Snake2(SpinorAfterKick)
          if(i%100==1):
               p=source.CalPorDegree(Spinor)
               #p=source.CalPorDegree(SpinorAfterKick)
               PorPlotX.append(GGamma)
               PorPlotY.append(p)
     else:
          K=IntGGamma
          SpinorAfterKick=source.ResonanceKick(Spinor,GGamma,K)
          Spinor=source.Snake2(SpinorAfterKick)
          if(i%100==1):
               p=source.CalPorDegree(Spinor)
               #p=source.CalPorDegree(SpinorAfterKick)
               PorPlotX.append(GGamma)
               PorPlotY.append(p)

#Draw the picture of the change of porlization degree
#print(PorPlotX)
print(PorPlotY)
plt.scatter(PorPlotX, PorPlotY)
plt.show()




