#!/usr/local/bin/python3.9
# -*- coding: UTF-8 -*-

import sys
import source
import matplotlib.pylab as pyl
import matplotlib.pyplot as plt
import numpy as np
import math
import copy
import os

#G=0.001159652 #electron
G=1.7928474 #proton

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
    

#read resonance data
ResonanceFile=parameters['ResonanceFile']
ResonanceFilePath="/Users/chentao/mywork_Duanz/SpinDynamics/ResonanceFile_2/"+ResonanceFile
f=open(ResonanceFilePath)
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
          SnakeStrength.append(float(SnakePara.split(" , ")[1].split("=")[1]))

          
          
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
  


if(parameters['Initialize']=='1'):
     
     Spinor=source.InitializeRandomPhase1(float(parameters['InitialPolarizationDegree']),1)

     SpinModule2=source.CalModules(Spinor)    #The modules of spinors should be 1 
     ParNum=len(SpinModule2)
     for i in range(ParNum):
          if(abs(SpinModule2[i]-1)>0.0000001):
               print('ERROR:Modules of Spinor is not normalized ')
               break

if(parameters['Initialize']=='2'):
     
     Spinor=source.InitializeRandomPhase2(float(parameters['InitialPolarizationDegree']),4)

     SpinModule3=source.CalModules(Spinor)    #The modules of spinors should be 1 
     ParNum=len(SpinModule3)
     for i in range(ParNum):
          if(abs(SpinModule3[i]-1)>0.0000001):
               print('ERROR:Modules of Spinor is not normalized ')
               break

if(parameters['Initialize']=='3'):
     
     Spinor=source.InitializeRandomPhase3(float(parameters['InitialPolarizationDegree']),32)

     SpinModule4=source.CalModules(Spinor)    #The modules of spinors should be 1 
     ParNum=len(SpinModule4)
     for i in range(ParNum):
          if(abs(SpinModule4[i]-1)>0.0000001):
               print('ERROR:Modules of Spinor is not normalized ')
               break

if(parameters['Initialize']=='0'):
     
     Spinor=source.InitializeAverage(float(parameters['InitialPolarizationDegree']),int(parameters['ParticleNum']))

     SpinModule4=source.CalModules(Spinor)    #The modules of spinors should be 1 
     ParNum=len(SpinModule4)
     for i in range(ParNum):
          if(abs(SpinModule4[i]-1)>0.0000001):
               print('ERROR:Modules of Spinor is not normalized ')
               break


#To rotate spinor towards the spin clost orbit within a partial snake
if(parameters['ShiftToSnakeCloseOrbit']=='1'):

    SnakeStrengthphi=SnakeStrength[0]

    #GGamma1=22.0334
    GGamma1=float(parameters['InitialGamma'])*G
    cc=math.cos(math.pi*GGamma1)*math.cos(SnakeStrengthphi/2)
    pivues=math.acos(cc)
    cosalpha1=0.
    cosalpha2=math.sin(SnakeStrengthphi/2)/math.sin(pivues)
    cosalpha3=(math.sin(math.pi*GGamma1)*math.cos(SnakeStrengthphi/2))/math.sin(pivues)
    S1=cosalpha1
    S2=cosalpha2
    S3=cosalpha3
    theta1=math.acos(S3)
    if(S2>=0):
         phi1=math.acos(S1/math.sin(theta1))
    else:
         phi1=2*math.pi-math.acos(S1/math.sin(theta1))
        
    source.TransferToN(Spinor,theta1,phi1)
    print('Sn======',source.CalSn(Spinor,theta1,phi1))

InitialDirection=source.CalDirectionofSpinor(Spinor)
print('Initial Direction',InitialDirection)

#Implement the acceleration  , It is correct for the single resonance model.
InitialGamma=float(parameters['InitialGamma'])
FinalGamma=float(parameters['FinalGamma'])
if(parameters['EnergyRisePerTurn']!='r'):
    EnergyRisePerTurn=float(parameters['EnergyRisePerTurn'])
Gamma=InitialGamma

CircleNum=0
ArcAngle=[]
ArcAngle.append(0)

if(True):
     ResonanceCount=0
     ResonanceCountForCal=0
     ResonanceNum=len(ResonanceLocationOrder)
     FindIfEnoughWidth='0'


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

               #Find the resonance that do not have enough width
               if(True):
                   if(ResonanceCount<ResonanceNum-2 and FindIfEnoughWidth=='1'):
                        LeftWidth =(ResonanceLocationOrder[ResonanceCount]-ResonanceLocationOrder[ResonanceCount-1])/2
                        RightWidth=(ResonanceLocationOrder[ResonanceCount+1]-ResonanceLocationOrder[ResonanceCount])/2
                        if(LeftWidth<5*abs(ResonanceData[ResonanceLocationOrder[ResonanceCount]]) or RightWidth<5*abs(ResonanceData[ResonanceLocationOrder[ResonanceCount]])):
                             print('There is not enough width for resonance location at : ', ResonanceLocationOrder[ResonanceCount])

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

                                                  
                         source.PartialResonanceKickIntrinsicResonance(Spinor,GGamma,ResonanceLocationOrder[ResonanceCountForCal],complex(ResonanceData[ResonanceLocationOrder[ResonanceCountForCal]]),inputtheta1,inputtheta2)
                             
                              
                         
                         ArcCount=ArcCount+1
     
                    if(LatticeSorting[i]=='Snake'):
                         
                         SnakeStrength_phi=SnakeStrength[SnakeCount]
                         SnakeDirection_phis=SnakeDirection[SnakeCount]

                         #Let the strength of snake varies with gamma when the condotion='True'
                         if(parameters['SnakeStrengthVarying']=='1'):
                             SnakeStrength_phi_VariesWithGamma=SnakeStrength_phi*19000/Gamma
                             source.Snake(Spinor,SnakeStrength_phi_VariesWithGamma,SnakeDirection_phis)
                         else:
                             source.Snake(Spinor,SnakeStrength_phi,SnakeDirection_phis)
     
                         SnakeCount=SnakeCount+1
               
     
               CircleNum=CircleNum+1    
               
               IfSaveP=CircleNum%int(parameters['OutputInterval'])
               if(parameters['OutputEveryTurnData']=='1' and IfSaveP==0):

                         isExist=os.path.exists('Results')
                         if not isExist:
                              os.makedirs('Results')
             
                         tune1=parameters['ResonanceFile'].split('_')[1]
                         FileName="Results/Result_"+tune1
                         fdata = open(FileName, 'a+')  
                         if(parameters['Initialize']=='0' or parameters['Initialize']=='1'):
                             p=source.CalSyAverage(Spinor)                          
                             S1=source.CalSxAverage(Spinor)   
                             S2=source.CalSsAverage(Spinor)

                         if(parameters['Initialize']=='2'):
                             p=source.CalSyAverage_Intrinsic(Spinor)                          
                             S1=source.CalSxAverage_Intrinsic(Spinor)   
                             S2=source.CalSsAverage_Intrinsic(Spinor)

                         if(parameters['Initialize']=='3'):
                             p=source.CalSyAverage_Intrinsic_Phase(Spinor)                          
                             S1=source.CalSxAverage_Intrinsic_Phase(Spinor)   
                             S2=source.CalSsAverage_Intrinsic_Phase(Spinor)

                         fdata.write(str(GGamma))
                         fdata.write(" ")

                         fdata.write(str(S1))  #additional
                         fdata.write(" ")
                         fdata.write(str(S2))
                         fdata.write(" ")

                         fdata.write(str(p))
                         fdata.write("\n")
                         fdata.close()
               if(parameters['EnergyRisePerTurn']!='r'):
                   Gamma=Gamma+EnergyRisePerTurn
               else:
                   Gamma=Gamma+(41462.6*math.sin(0.000400134*CircleNum))/2996

                    
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
     #_4piq=math.pi*abs(ResonanceStrength)*abs(ResonanceStrength)/(2*alpha)

     FSFileName=parameters['FSDataFileName']
     fdata = open(FSFileName, 'a+')  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加


     p=source.CalSyAverage_Intrinsic_Phase(Spinor)
     p_general=p/float(parameters['InitialPolarizationDegree'])

     fdata.write(str(alpha))
     fdata.write(" ")

     fdata.write(str(p_general))

     fdata.write("\n")
     fdata.close()

FinalDirection=source.CalDirectionofSpinor(Spinor)
#print('Final Spinor',Spinor)
print('Final Direction',FinalDirection)




if(False):
     fdata = open('FinalDirection', 'a+')  


     Len=len(FinalDirection)
     for i in range(Len):
          fdata.write(str(FinalDirection[i][0]))
          fdata.write(" ")
          fdata.write(str(FinalDirection[i][1]))
          fdata.write("\n")

     fdata.close()

