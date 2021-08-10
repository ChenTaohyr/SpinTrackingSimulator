#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import source
      
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
#print(Spinor)
G=0.001159652
GGamma=G*1
SpinorAfterArc=source.Arc(Spinor,GGamma)
Spinor2=source.Snake(SpinorAfterArc)
#print(Spinor2)