#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import source
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
import math
import copy

G=0.001159652

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
    


#initialize the beam
#Spinor=source.InitializeRandomPhase(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))
#Spinor=source.Initialize(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))

#print('initial spinor:',Spinor)
#DirectionInitial=source.CalDirectionofSpinor(Spinor)
#print('initial direction:',DirectionInitial)

#read resonance data
ResonanceFile=parameters['ResonanceFile']

f=open(ResonanceFile)
ResonanceData={}

while True:                      
         line=f.readline()
         line=line.strip()
         if not line:
              break
         else:
              ResonanceStrength=float(line.split(' ')[1])+1j*float(line.split(' ')[2])   #Read and save resonance strength as complex
              #print(ResonanceStrength)
              ResonanceData[float(line.split(' ')[0])] =ResonanceStrength
                       
f.close() 


#read lattice data
LatticeFile=parameters['LatticeFile']
#print(ResonanceFile,type(ResonanceFile))
f=open(LatticeFile)
Lattice=[]
LatticeSorting=[]
while True:                      
         line=f.readline()
         line=line.strip()
         if not line:
              break
         else:
              Lattice.append(line)
              LatticeSorting.append(line.split(": ")[0])
                       
f.close() 


#To read and save lattice information
LatticeNum=len(Lattice)
ArcData=[]
#ArcCount=0
SnakeDirection=[]
SnakeStrength=[]
#SnakeCount=0
for i in range(LatticeNum):
     LatticeName=Lattice[i].split(": ")[0]
     if(LatticeName=="Snake"):
          SnakePara=Lattice[i].split(": ")[1]
          SnakeDirection.append(float(SnakePara.split(" , ")[0].split("=")[1]))
          #Direction_phis=float(SnakePara.split(" , ")[0].split("=")[1])
          SnakeStrength.append(float(SnakePara.split(" , ")[1].split("=")[1]))
          #SnakeStrength=float(SnakePara.split(" , ")[1].split("=")[1])
          
          
     if(LatticeName=="Arc"):
          ArcData.append(float(Lattice[i].split(": ")[1].split("=")[1]))
        

#initialize the beam or generate a test spin
if(parameters['GenerateSpin']=='1'):
     InitialSpinDirection_phi=float(parameters['InitialSpinDirection_phi'])
     InitialSpinDirection_theta=float(parameters['InitialSpinDirection_theta'])
     Spinor=source.GenerateSpin(InitialSpinDirection_phi,InitialSpinDirection_theta)

     SpinModule1=source.CalModules(Spinor)    #The modules of spinors should be 1 
     ParNum=len(SpinModule1)
     for i in range(ParNum):
          if(abs(SpinModule1[i]-1)>0.0000001):
               print('ERROR:Modules of Spinor is not normalized ')
               break


#Spinor=source.GeneratePartialSnakeSpin(SnakeStrength,GGamma)


if(parameters['Initialize']=='1'):
     
     #Spinor=source.InitializeRandomPhase(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))
     Spinor=source.Initialize(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))

     SpinModule2=source.CalModules(Spinor)    #The modules of spinors should be 1 
     ParNum=len(SpinModule2)
     for i in range(ParNum):
          if(abs(SpinModule2[i]-1)>0.0000001):
               print('ERROR:Modules of Spinor is not normalized ')
               break

InitialDirection=source.CalDirectionofSpinor(Spinor)
print('Initial Direction',InitialDirection)

#Implement the acceleration  , It is correct for the single resonance model.
InitialGamma=int(parameters['InitialGamma'])
FinalGamma=int(parameters['FinalGamma'])
EnergyRisePerTurn=float(parameters['EnergyRisePerTurn'])
Gamma=InitialGamma

CirleNum=0
ArcAngle=[]
ArcAngle.append(0)
#print(ArcData)
while (Gamma<FinalGamma):
          GGamma=G*Gamma
          ArcCount=0
          SnakeCount=0
          for i in range(LatticeNum):
               

               if(LatticeSorting[i]=='Arc'):
                    
                    theta1=ArcAngle[ArcCount]
                    theta2=theta1+ArcData[ArcCount]
                    ArcAngle.append(theta2)
                    
                    for j in ResonanceData:
                         source.PartialResonanceKick(Spinor,GGamma,j,complex(ResonanceData[j]),theta1,theta2)
                    
                    #print('Arc cross',theta1,theta2)

                    ArcCount=ArcCount+1

               if(LatticeSorting[i]=='Snake'):
                    
                    SnakeStrength_phi=SnakeStrength[SnakeCount]
                    SnakeDirection_phis=SnakeDirection[SnakeCount]

                    source.Snake(Spinor,SnakeStrength_phi,SnakeDirection_phis)

                    SnakeCount=SnakeCount+1
          

          CirleNum=CirleNum+1    
          Gamma=Gamma+EnergyRisePerTurn


SpinModule3=source.CalModules(Spinor)
ParNum=len(SpinModule3)
for i in range(ParNum):
     if(abs(SpinModule3[i]-1)>0.0000001):
          print('ERROR:Modules of Spinor is not normalized ')
          break


print('Finished accelartion after %d Circles' %CirleNum)


#calcalute for verify F-S Equation and simulation
if(parameters['OutputCalibrateFSEquationData']=='1'):
     alpha=G*EnergyRisePerTurn/(2*math.pi)
     _4piq=math.pi*abs(ResonanceStrength)*abs(ResonanceStrength)/(2*alpha)
     #print('4piq',_4piq)

     fdata = open("FSData_test2.txt", 'a+')  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加

     p=source.CalPorDegree(Spinor)
     fdata.write(str(_4piq))
     fdata.write(" ")
     fdata.write(str(p))
     fdata.write("\n")
     print("Successfully print", fdata)
     fdata.close()
FinalDirection=source.CalDirectionofSpinor(Spinor)
print('Final Spinor',Spinor)
print('Final Direction',FinalDirection)
#delta=G*Gamma-int(G*Gamma)
#source.GenerateSpin(math.pi*(5-delta)+float(parameters['SnakeDirection_phis']),math.pi/2,Spinor)
#source.GenerateSpin(float(parameters['SnakeDirection_phis']),math.pi/2,Spinor)
#source.GeneratePartialSnakeSpin(float(parameters['SnakeStrength_phi']),G*Gamma,Spinor)
#source.GenerateSpin(1.1,math.pi/2,Spinor)
'''
print('Spinor on n direction',Spinor)
Direction2=source.CalDirectionofSpinor(Spinor)
print('Direction of n Spinor:',Direction2)
'''

'''
xp2=source.CalPorDegreeX(Spinor)
print('X Polarization Degree after Transform',xp2)
#print('Spinor After Transform',Spinor)
'''


'''

CirleNum=0
while (Gamma<FinalGamma):
          GGamma=G*Gamma
          theta1=math.pi
          theta2=2*math.pi

          for i in ResonanceData:
               source.PartialResonanceKick(Spinor,GGamma,i,complex(ResonanceData[i]),0,theta1)
               
          if (parameters['UseSnake']=='1'):
               source.Snake(Spinor,float(parameters['SnakeStrength_phi']),float(parameters['SnakeDirection_phis']))
              
          for i in ResonanceData:
               source.PartialResonanceKick(Spinor,GGamma,i,complex(ResonanceData[i]),theta1,theta2)     
               
          CirleNum=CirleNum+1    
          Gamma=Gamma+EnergyRisePerTurn

print('final spinor', Spinor)
print('Modules of the spinors', source.CalModules(Spinor))
p=source.CalPorDegree(Spinor)
print('final polarization degree',p)

Direction3=source.CalDirectionofSpinor(Spinor)
print('Final Direction of Spinor',Direction3)
'''




'''
xp3=source.CalPorDegreeX(Spinor)
print('Final X Polarization Degree ',xp3)

yp3=source.CalPorDegreeY(Spinor)
print('Final Y Polarization Degree',yp3)
print(xp3*xp3+yp3*yp3+p*p)
'''

'''
print('Finished accelartion after %d Circles' %CirleNum)

#calcalute for verify F-S Equation and simulation
alpha=G*EnergyRisePerTurn/(2*math.pi)
_4piq=math.pi*abs(ResonanceStrength)*abs(ResonanceStrength)/(2*alpha)
print('4piq',_4piq)

fdata = open("FSData.txt", 'a+')  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加


fdata.write(str(_4piq))
fdata.write(" ")
fdata.write( str(p))
fdata.write("\n")
print("Successfully print", fdata)
fdata.close()
'''



