#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
import math
      
file_name = sys.argv[1]           #Get input file

f=open(file_name)
FSCalData4piq=[]
FSCalDataP=[]
while True:                      #Read every parameters and save them in dir 
         line=f.readline()
         line=line.strip()
         if not line:
              break
         else:
             FSCalData4piq.append(float(line.split(' ')[0]))
             FSCalDataP.append(float(line.split(' ')[1]))

             
             
f.close()   

#print(FSCalData4piq)
#print(FSCalDataP)


n=np.linspace(-2.8, 1.5, 500)
xn=[]
yn=[]
for i in n:
    x=10**i
    xn.append(x)
    y=2*math.exp(-x)-1
    yn.append(y)


plt.axes(xscale = "log") 
plt.scatter(FSCalData4piq, FSCalDataP)
plt.plot(xn,yn,label='Theoretical curve',color='g')

plt.xlabel('4piq')
plt.ylabel('P_FS')
plt.title('FS Formula vs. Simulation')
plt.show()