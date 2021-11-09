#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys

import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
import math
import copy

f=open('Result_test.txt')

Sn_NoResonance=[]

while True:                      
         line=f.readline()
         line=line.strip()
         if not line:

             break
    
         else:
             Sn_NoResonance.append([float(line.split(' ')[0]),float(line.split(' ')[1]),float(line.split(' ')[2]),float(line.split(' ')[3])])
'''
with open('Result_test.txt','r') as f:
    for line in f.readlines(8669:8679):
        line.strip()
        Sn_NoResonance.append([float(line.split(' ')[0]),float(line.split(' ')[1]),float(line.split(' ')[2]),float(line.split(' ')[3])])
'''
f.close() 


Tune=[]
for i in range(20):
    tune=0.01*i+8.8
    Tune.append(tune)

Result=[]
for j in range(20):
    UsedTune=str(Tune[j])
    while(len(UsedTune)<4):
        UsedTune+='0'
    FileName="Result_"+UsedTune+".txt"
    f=open(FileName)
    Sn_Resonance=[]

    while True:                      
        line=f.readline()
        line=line.strip()
        if not line:
            break   
        else:
            Sn_Resonance.append([float(line.split(' ')[0]),float(line.split(' ')[1]),float(line.split(' ')[2]),float(line.split(' ')[3])])  
    '''
    for line in f.readlines()[8669:8679]:
        line=line.strip()
        Sn_Resonance.append([float(line.split(' ')[0]),float(line.split(' ')[1]),float(line.split(' ')[2]),float(line.split(' ')[3])])

'''
    f.close() 
    InnerProduct=[]
    for i in range(13189,13199):
        InnerProduct.append(Sn_Resonance[i][1]*Sn_NoResonance[i][1]+Sn_Resonance[i][2]*Sn_NoResonance[i][2]+Sn_Resonance[i][3]*Sn_NoResonance[i][3])
    sum=0

    for i in range(10):
        sum=sum+InnerProduct[i]
    Result.append(sum/10)

Data=open('Data.txt','a+')
for i in range(20):
    Data.write(str(Tune[i]))
    Data.write(' ')
    Data.write(str(Result[i]))
    Data.write('\n')
Data.close()

plt.plot(Tune, Result)
#plt.scatter(Tune,Result,s=1)
plt.ylim(-1,1)
plt.grid()
plt.xlabel('Betatron Tune')
plt.ylabel('Polarization')
plt.title('Polarization vs. BetatronTune')
plt.show()

    