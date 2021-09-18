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
ResonanceLocationOrder=[]

while True:                      
         line=f.readline()
         line=line.strip()
         if not line:
              break
         else:
              ResonanceStrength=float(line.split('\t')[2])+1j*float(line.split('\t')[3])   #Read and save resonance strength as complex

              ResonanceData[float(line.split('\t')[0])] =ResonanceStrength
              ResonanceLocationOrder.append(float(line.split('\t')[0]))
                       
f.close() 
ResonanceLocationOrder.append(99999.)     #Just for convenience in later calculation ,no practical meaning

#read lattice data
LatticeFile=parameters['LatticeFile']
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
SnakeDirection=[]
SnakeStrength=[]
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

#For testing of  partial snake, use when parameters 'Initialize=0'
#Spinor=source.GeneratePartialSnakeSpin(1.57079632679489661923,22.0334)     


if(parameters['Initialize']=='1'):
     
     Spinor=source.InitializeRandomPhase(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))
     #Spinor=source.Initialize(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))

     SpinModule2=source.CalModules(Spinor)    #The modules of spinors should be 1 
     ParNum=len(SpinModule2)
     for i in range(ParNum):
          if(abs(SpinModule2[i]-1)>0.0000001):
               print('ERROR:Modules of Spinor is not normalized ')
               break


#For testing of a different initialize method .Use when parameters'Initialize =0'
'''
Spinor1=source.InitializeRandomPhase(1.,50)
Spinor2=source.InitializeRandomPhase(0.,50)
Spinor3=source.InitializeRandomPhase(0.9,50)
Spinor4=source.InitializeRandomPhase(0.1,50)
Spinor5=source.InitializeRandomPhase(0.8,50)
Spinor6=source.InitializeRandomPhase(0.2,50)
Spinor7=source.InitializeRandomPhase(0.7,50)
Spinor8=source.InitializeRandomPhase(0.3,50)
Spinor9=source.InitializeRandomPhase(0.6,50)
Spinor10=source.InitializeRandomPhase(0.4,50)
Spinor11=source.InitializeRandomPhase(0.5,50)
Spinor12=source.InitializeRandomPhase(0.5,50)
Spinor=Spinor1+Spinor2+Spinor3+Spinor4+Spinor5+Spinor6+Spinor7+Spinor8+Spinor9+Spinor10+Spinor11+Spinor12
'''




InitialDirection=source.CalDirectionofSpinor(Spinor)
print('Initial Direction',InitialDirection)

#Implement the acceleration  , It is correct for the single resonance model.
InitialGamma=int(parameters['InitialGamma'])
FinalGamma=int(parameters['FinalGamma'])
EnergyRisePerTurn=float(parameters['EnergyRisePerTurn'])
Gamma=InitialGamma

CircleNum=0
ArcAngle=[]
ArcAngle.append(0)
if(parameters['SingleResonance']=='1'):
     while (Gamma<FinalGamma):
               GGamma=G*Gamma
               ArcCount=0
               SnakeCount=0
               for i in range(LatticeNum):
                    
     
                    if(LatticeSorting[i]=='Arc'):
                         
                         theta1=ArcAngle[ArcCount]
                         theta2=theta1+ArcData[ArcCount]
                         ArcAngle.append(theta2)
     
                         inputtheta1=theta1+2*math.pi*CircleNum
                         inputtheta2=theta2+2*math.pi*CircleNum
                         
                         for j in ResonanceData:
                              
                              source.PartialResonanceKick(Spinor,GGamma,j,complex(ResonanceData[j]),inputtheta1,inputtheta2)
                              
                         
                         ArcCount=ArcCount+1
     
                    if(LatticeSorting[i]=='Snake'):
                         
                         SnakeStrength_phi=SnakeStrength[SnakeCount]
                         SnakeDirection_phis=SnakeDirection[SnakeCount]
     
                         source.Snake(Spinor,SnakeStrength_phi,SnakeDirection_phis)
     
                         SnakeCount=SnakeCount+1
               
     
               CircleNum=CircleNum+1    
               
               Gamma=Gamma+EnergyRisePerTurn



if(parameters['MultipleResonance']=='1'):
     ResonanceCount=0
     ResonanceCountForCal=0
     ResonanceNum=len(ResonanceLocationOrder)
     FindIfEnoughWidth='0'

     if(parameters['OutputEveryTurnData']=='1'):
          P_GGamma=[]

     while (Gamma<FinalGamma):
               GGamma=G*Gamma

               

               while(GGamma>ResonanceLocationOrder[ResonanceCount]):
                    ResonanceCount=ResonanceCount+1
                    FindIfEnoughWidth='1'

               ResonanceCountForCal=copy.deepcopy(ResonanceCount)
               
               #During the acceleration ,only nearest spin resonance is considered
               if(ResonanceCount>0 and ResonanceCount<ResonanceNum-1):    
                    deltaLeft =abs(GGamma-ResonanceLocationOrder[ResonanceCount-1])
                    deltaRight=abs(GGamma-ResonanceLocationOrder[ResonanceCount])
                    if(deltaRight>deltaLeft):
                         ResonanceCountForCal=ResonanceCountForCal-1

               #if(ResonanceCount<ResonanceNum-2 and FindIfEnoughWidth=='1'):          #Find the resonance that do not have enough width
               #     LeftWidth =(ResonanceLocationOrder[ResonanceCount]-ResonanceLocationOrder[ResonanceCount-1])/2
               #     RightWidth=(ResonanceLocationOrder[ResonanceCount+1]-ResonanceLocationOrder[ResonanceCount])/2
               #     if(LeftWidth<5*abs(ResonanceData[ResonanceLocationOrder[ResonanceCount]]) or RightWidth<5*abs(ResonanceData[ResonanceLocationOrder[ResonanceCount]])):
               #          print('There is not enough width for resonance location at : ',ResonanceLocationOrder[ResonanceCount])

               if(ResonanceCount==ResonanceNum-1):
                    ResonanceCountForCal=ResonanceCountForCal-1

               FindIfEnoughWidth='0'
               #The above code is to find which resonance should be included in calculation

               ArcCount=0
               SnakeCount=0
               for i in range(LatticeNum):
                    
     
                    if(LatticeSorting[i]=='Arc'):
                         
                         theta1=ArcAngle[ArcCount]
                         theta2=theta1+ArcData[ArcCount]
                         ArcAngle.append(theta2)
     
                         inputtheta1=theta1+2*math.pi*CircleNum
                         inputtheta2=theta2+2*math.pi*CircleNum

                         #To move resonance location ,additional module.
                         #if(abs(ResonanceLocationOrder[ResonanceCountForCal]-int(ResonanceLocationOrder[ResonanceCountForCal])-0.21)<0.000000001):
                         #     ResoananceK=ResonanceLocationOrder[ResonanceCountForCal]+0.04
                         #if(abs(ResonanceLocationOrder[ResonanceCountForCal]-int(ResonanceLocationOrder[ResonanceCountForCal])-0.79)<0.000000001):
                         #     ResoananceK=ResonanceLocationOrder[ResonanceCountForCal]-0.04                    
                         #source.PartialResonanceKick(Spinor,GGamma,ResoananceK,complex(ResonanceData[ResonanceLocationOrder[ResonanceCountForCal]]),inputtheta1,inputtheta2)


                              
                         source.PartialResonanceKick(Spinor,GGamma,ResonanceLocationOrder[ResonanceCountForCal],complex(ResonanceData[ResonanceLocationOrder[ResonanceCountForCal]]),inputtheta1,inputtheta2)
                              
                         
                         ArcCount=ArcCount+1
     
                    if(LatticeSorting[i]=='Snake'):
                         
                         SnakeStrength_phi=SnakeStrength[SnakeCount]
                         SnakeDirection_phis=SnakeDirection[SnakeCount]
     
                         source.Snake(Spinor,SnakeStrength_phi,SnakeDirection_phis)
     
                         SnakeCount=SnakeCount+1
               
     
               CircleNum=CircleNum+1    
               
               IfSaveP=CircleNum%int(parameters['OutputInterval'])
               if(parameters['OutputEveryTurnData']=='1' and IfSaveP==0):
                         fdata = open("P_vs_GGamma.txt", 'a+')  

                         p=source.CalPorDegree(Spinor)
                         fdata.write(str(GGamma))
                         fdata.write(" ")
                         fdata.write(str(p))
                         fdata.write("\n")
                         fdata.close()
               
               Gamma=Gamma+EnergyRisePerTurn

                    






SpinModule3=source.CalModules(Spinor)
ParNum=len(SpinModule3)
for i in range(ParNum):
     if(abs(SpinModule3[i]-1)>0.0000001):
          print('ERROR:Modules of Spinor is not normalized ')
          break


print('Finished accelartion after %d Circles' %CircleNum)


#calcalute for verify F-S Equation and simulation
if(parameters['OutputCalibrateFSEquationData']=='1'):
     alpha=G*EnergyRisePerTurn/(2*math.pi)
     _4piq=math.pi*abs(ResonanceStrength)*abs(ResonanceStrength)/(2*alpha)

     FSFileName=parameters['FSDataFileName']
     fdata = open(FSFileName, 'a+')  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加

     p=source.CalPorDegree(Spinor)
     p_general=p/float(parameters['InitialPolarizationDegree'])
     #PP=source.Cal0_3PolarizationDegree(Spinor)
     fdata.write(str(_4piq))
     fdata.write(" ")
     #fdata.write(str(p))
     #fdata.write(str(PP))
     fdata.write(str(p_general))

     fdata.write("\n")
     #print("Successfully print", fdata)
     fdata.close()

if(parameters['OutputEpsilon_PData']=='1'):
     #alpha=G*EnergyRisePerTurn/(2*math.pi)
     #_4piq=math.pi*abs(ResonanceStrength)*abs(ResonanceStrength)/(2*alpha)
     epsilon=abs(ResonanceStrength)
     #print('4piq',_4piq)
    
     fdata = open("Epsilon_P.txt", 'a+') 

     p=source.CalPorDegree(Spinor)
     fdata.write(str(epsilon))
     fdata.write(" ")
     fdata.write(str(p))
     fdata.write("\n")
     #print("Successfully print", fdata)
     fdata.close()

FinalDirection=source.CalDirectionofSpinor(Spinor)
print('Final Spinor',Spinor)
print('Final Direction',FinalDirection)






