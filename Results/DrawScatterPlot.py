#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
import math
      
file_name = sys.argv[1]           #Get input file

f=open(file_name)
GGamma=[]
Pz=[]
Px=[]
Py=[]
while True:                      #Read every parameters and save them in dir 
         line=f.readline()
         line=line.strip()
         if not line:
            break
         else:
            GGamma.append(float(line.split(' ')[0]))
            Pz.append(float(line.split(' ')[3]))
            Px.append(float(line.split(' ')[1]))
            Py.append(float(line.split(' ')[2]))

             
             
f.close()   





plt.scatter(GGamma, Px,s=0.1,color='g',label='Px')
plt.scatter(GGamma, Py,s=0.1,color='r',label='Py')
plt.scatter(GGamma, Pz,s=1,color='b',label='Pz')
#plt.ylim(-1,1.8)
plt.legend()
plt.xlabel('aGamma')
plt.ylabel('Polarization')
plt.title('polarization vs. aGamma')
plt.show()
