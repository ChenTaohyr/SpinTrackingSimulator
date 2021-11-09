#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys

import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
import math
import copy



f=open('Result_8.95.txt')
Sn_Resonance=[]
while True:                      
     line=f.readline()
     line=line.strip()
     if not line:
         break   
     else:
         Sn_Resonance.append([float(line.split(' ')[0]),float(line.split(' ')[1]),float(line.split(' ')[2]),float(line.split(' ')[3])])
            
             
             
f.close()   

f=open('Result_test.txt')
Sn_NoResonance=[]
while True:                      
         line=f.readline()
         line=line.strip()
         if not line:

             break
    
         else:
             Sn_NoResonance.append([float(line.split(' ')[0]),float(line.split(' ')[1]),float(line.split(' ')[2]),float(line.split(' ')[3])])
            
                    
f.close()  

Len=len(Sn_NoResonance)
InnerProduct=[]
Gamma=[]
for i in range(Len):
    InnerProduct.append(Sn_Resonance[i][1]*Sn_NoResonance[i][1]+Sn_Resonance[i][2]*Sn_NoResonance[i][2]+Sn_Resonance[i][3]*Sn_NoResonance[i][3])
    if(i>8660):
        print(InnerProduct[i])
    Gamma.append(Sn_Resonance[i][0])


plt.ylim([-1.5,1.5])
plt.scatter(Gamma, InnerProduct,s=1)


plt.xlabel('aGamma')
plt.ylabel('InnerProduct')
plt.title('Projection on spin close orbit')
plt.show()