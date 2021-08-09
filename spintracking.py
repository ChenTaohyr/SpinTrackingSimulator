#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import source.py
      
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
    
print(parameters)
print(parameters['InitialPolarizationDegree'])
Initialize(parameters['InitialPolarizationDegree'])