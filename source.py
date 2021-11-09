# -*- coding: UTF-8 -*-
import math
import cmath
import random
import copy
G=0.001159652

#Initialize of the beam
def Initialize(InitialPolarizationDegree,ParticleNum):   #Wrong if initial polarization degree is not zero and not enough particle
    #print 'Initializing...'
    #print('InitialPolarizationDegree ' ,InitialPolarizationDegree)
    #print('particlenum ' ,ParticleNum)
#A simples‘t initialization for test (21-8-10)

#for a polarization degree P beam ,assume all electrons are spin up or spin down ,
#the number of spin up  electrons is N* (P+1)/2, in this case assume spinupNum is integer
    #SpinUpNum=((InitialPolarizationDegree+1)/2)*ParticleNum
    Spinor=[]
    #for i in range(ParticleNum):
    #        if i < SpinUpNum:
    #           Spinor.append([complex(1),complex(0)])
    #        else:
    #            Spinor.append([complex(0),complex(1)])


    #Modified initialize program
    for i in range(ParticleNum):
       
        up=math.sqrt((InitialPolarizationDegree+1)/2)
        down=math.sqrt((1-InitialPolarizationDegree)/2)
        Spinor.append([complex(up),complex(down)])

    #print('Initial Spinor',Spinor)
    #print 'Initialization done'
    
    return Spinor

#For a specified porlaration degree,all particles are assign to the same up and down compnents -
#-and a  random phase factor 

#InitializeRandomPhase3 initialize 32 particles with different betatron amplitude and betatron phase
def InitializeRandomPhase3(InitialPolarizationDegree,ParticleNum):
    #print 'Initializing...'
    #print('InitialPolarizationDegree ' ,InitialPolarizationDegree)
    #print('particlenum ' ,ParticleNum)
    factor=[0.2671,0.94,1.9617,4.1589]
    phase=[0.,0.25,0.5,0.75,1.,1.25,1.5,1.75]

    Spinor=[]
    for i in range(ParticleNum):
        RandomPhase1=2j*random.random()*math.pi
        RandomPhase3=2j*random.random()*math.pi
        up=math.sqrt((InitialPolarizationDegree+1)/2)
        down=math.sqrt((1-InitialPolarizationDegree)/2)
        #Spinor.append([up*cmath.exp(RandomPhase1),down*cmath.exp(RandomPhase2)])
        Spinor.append([up*cmath.exp(RandomPhase1)*cmath.exp(RandomPhase3),down*cmath.exp(RandomPhase3)])    #another approach to generate random phase spinor
        
        #Add an action and betatron phase for every particle 
    particleconut=0  
    for j in range(4):
        for k in range(8):
            Spinor[particleconut].append(factor[j])
            Spinor[particleconut].append(phase[k])
            particleconut=particleconut+1     
    return Spinor

#InitializeRandomPhase2 initialize 4 particles with different betatron amplitude . No betatron phase average.
def InitializeRandomPhase2(InitialPolarizationDegree,ParticleNum):

    factor=[0.2671,0.94,1.9617,4.1589]
    Spinor=[]
    for i in range(ParticleNum):
        RandomPhase1=2j*random.random()*math.pi
        RandomPhase3=2j*random.random()*math.pi
        up=math.sqrt((InitialPolarizationDegree+1)/2)
        down=math.sqrt((1-InitialPolarizationDegree)/2)
        #Spinor.append([up*cmath.exp(RandomPhase1),down*cmath.exp(RandomPhase2)])
        Spinor.append([up*cmath.exp(RandomPhase1)*cmath.exp(RandomPhase3),down*cmath.exp(RandomPhase3)])   
        Spinor[i].append(factor[i])
        Spinor[i].append(0)
 
    return Spinor

#InitializeRandomPhase1 use 1 particle. intrinsic resonance is considered as imperfection resonance.
def InitializeRandomPhase1(InitialPolarizationDegree,ParticleNum):
    Spinor=[]
    for i in range(ParticleNum):
        RandomPhase1=2j*random.random()*math.pi
        RandomPhase3=2j*random.random()*math.pi
        up=math.sqrt((InitialPolarizationDegree+1)/2)
        down=math.sqrt((1-InitialPolarizationDegree)/2)
        Spinor.append([up*cmath.exp(RandomPhase1)*cmath.exp(RandomPhase3),down*cmath.exp(RandomPhase3),1,0])  
 
    return Spinor
##This initialization method let the phase of particles uniformly distribute in 0 to 2pi ,to get best average properties
def InitializeAverage(InitialPolarizationDegree,ParticleNum):
    Spinor=[]
    PhaseInterval=1./(ParticleNum+1)
    PhaseNumber=[]
    for i in range(ParticleNum):
        PhaseNumber.append((i+1)*PhaseInterval)


    for i in range(ParticleNum):
        RandomPhase1=2j*PhaseNumber[i]*math.pi

        RandomPhase3=2j*random.random()*math.pi
        up=math.sqrt((InitialPolarizationDegree+1)/2)
        down=math.sqrt((1-InitialPolarizationDegree)/2)
        #Spinor.append([up*cmath.exp(RandomPhase1),down*cmath.exp(RandomPhase2)])
        Spinor.append([up*cmath.exp(RandomPhase1)*cmath.exp(RandomPhase3),down*cmath.exp(RandomPhase3),1,0])    #another approach to generate random phase spinor
           
    #print('Initial Spinor',Spinor)
    #print 'Initialization done'

    return Spinor






    

#Generate a spinor with Azimuth angle phi and Polar angle theta
#only for test ,only change the first spinor
def GenerateSpin(phi,theta):
    Spinor=[]
    Spinor.append([complex(math.cos(theta/2)),math.sin(theta/2)*cmath.exp(1j*phi)])
    #Spinor[0][0]=complex(math.cos(theta/2))
    #Spinor[0][1]=math.sin(theta/2)*cmath.exp(1j*phi)
    return Spinor

#Arc with angle 2pi,without any resonance

def Arc(Spinor,GGamma):
    Length=len(Spinor)
    for i in range(Length):
        
        Spinor[i][0]=Spinor[i][0]*(math.cos(GGamma*math.pi)-math.sin(GGamma*math.pi)*1j)
        Spinor[i][1]=Spinor[i][1]*(math.cos(GGamma*math.pi)+math.sin(GGamma*math.pi)*1j)
        
    return 


#A general snake module
#the snake axis direction is (cos[phis] ,sin[phis] , 0)
#phis varies from -pi to pi,phi from 0 to pi.
def Snake(Spinor,phi,phis):
    '''
    cc=math.cos((phi/2)*math.cos(phis))
    cs=math.cos((phi/2)*math.sin(phis))
    ss=math.sin((phi/2)*math.sin(phis))
    sc=math.sin((phi/2)*math.cos(phis))  #this calculation is totally wrong!
    '''
    m11=math.cos(phi/2)
    m12=-1j*math.sin(phi/2)*math.cos(phis)-math.sin(phis)*math.sin(phi/2)
    m21=-1j*math.sin(phi/2)*math.cos(phis)+math.sin(phis)*math.sin(phi/2)
    m22=math.cos(phi/2)
    Length=len(Spinor)

    for i in range(Length):
        a=Spinor[i][0]
        Spinor[i][0]=m11*Spinor[i][0]+m12*Spinor[i][1]
        Spinor[i][1]=a*m21+m22*Spinor[i][1]

    #return Spinor
    return
  



#rotate into resonance precessing frame ,apply the resonance kick then rotate back to particle rest frame
####(the strength of resonance is replaced by a estimated value of 0.002*GGamma )####deleted####
#eplison is the strength of resonance ,it is a complex
#The calculation is based on the Spin Transfer Matrix of constant GGamma ,suitable for all kinds of resonance
#The resonance kick is applied in a complete turn ie. theta from 0 to 2pi
def ResonanceKick(Spinor,GGamma,K,eplison):
    #eplison=GGamma*0.002
    delta=K-GGamma
    lamda=math.sqrt(delta*delta+abs(eplison)*abs(eplison))
    b=(abs(eplison)*math.sin(lamda*math.pi))/lamda
    a=math.sqrt(1-b*b)

    if (lamda-int(lamda)>0.5):       #Fix the error that arctan(Tan(x)) may lost some phase of a (integer*pi)
        AngleNum=int(lamda+1)
    else:
        AngleNum=int(lamda)

    c=math.atan((delta*math.tan(lamda*math.pi))/lamda)+AngleNum*math.pi
    d=-1*cmath.phase(eplison)
    
    Length=len(Spinor)
    for i in range(Length):
        
        x=Spinor[i][0]
        Spinor[i][0]=Spinor[i][0]*a*cmath.exp((c-K*math.pi)*1j)+1j*b*Spinor[i][1]*cmath.exp(-1j*(d+K*math.pi))#!!!Here pi should be 2pi!!!
        Spinor[i][1]=x*(1j)*b*cmath.exp(1j*(d+K*math.pi))+Spinor[i][1]*a*cmath.exp(-1j*(c-K*math.pi))
       

    return
#A more general module that consist of initial and final angle
def PartialResonanceKickIntrinsicResonance(Spinor,GGamma,K,eplison,thetai,thetaf):
    Length=len(Spinor)
    RealEplison=copy.deepcopy(eplison) 
    for i in range(Length):
        if(abs(K-int(K))>0.000001):  #To verify which is intrinsic resonance
        
            eplison2=RealEplison*math.sqrt(Spinor[i][2])*cmath.exp(1j*Spinor[i][3])
        else:
            eplison2=RealEplison*cmath.exp(1j*Spinor[i][3])
        


        delta=K-GGamma
        lamda=math.sqrt(delta*delta+abs(eplison2)*abs(eplison2))
        b=(abs(eplison2)*math.sin(lamda*(thetaf-thetai)/2))/lamda
        a=math.sqrt(1-b*b)
    


        cos_phi=math.cos(lamda*(thetaf-thetai)/2)
        if (cos_phi>=0):
            AngleNum=0

        else:
            AngleNum=1
    

        c=math.atan((delta*math.tan(lamda*(thetaf-thetai)/2))/lamda)+AngleNum*math.pi

        d=-1*cmath.phase(eplison2)
        
        x=Spinor[i][0]
        Spinor[i][0]=Spinor[i][0]*a*cmath.exp((c-K*(thetaf-thetai)/2)*1j)+1j*b*Spinor[i][1]*cmath.exp(-1j*(d+K*(thetaf+thetai)/2))
        Spinor[i][1]=x*(1j)*b*cmath.exp(1j*(d+K*(thetaf+thetai)/2))+Spinor[i][1]*a*cmath.exp(-1j*(c-K*(thetaf-thetai)/2))
       

    return


#Calculate polarization degree
#polarization degree=<<Sigma3>> --averaged by every particle
def CalSyAverage(Spinor):

    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        sigmai=abs(Spinor[i][0])*abs(Spinor[i][0])-abs(Spinor[i][1])*abs(Spinor[i][1])
        sigma.append(sigmai)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/Length
    #print(sigma)

    return Pordegree

def CalSyAverage_Intrinsic_Phase(Spinor):

    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        sigmai=(abs(Spinor[i][0])*abs(Spinor[i][0])-abs(Spinor[i][1])*abs(Spinor[i][1]))*0.5*math.exp((-1*Spinor[i][2])/2)
        sigma.append(sigmai)


    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/8


    return Pordegree

def CalSyAverage_Intrinsic(Spinor):

    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        sigmai=(abs(Spinor[i][0])*abs(Spinor[i][0])-abs(Spinor[i][1])*abs(Spinor[i][1]))*0.5*math.exp((-1*Spinor[i][2])/2)
        sigma.append(sigmai)


    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum


    return Pordegree


def CalSy(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        sigmai=abs(Spinor[i][0])*abs(Spinor[i][0])-abs(Spinor[i][1])*abs(Spinor[i][1])
        sigma.append(sigmai)



    return sigma



#To calculate the modules of Spinors 
def CalModules(Spinor):
    Length=len(Spinor)
    module=[]
    for i in range(Length):
        Module=abs(Spinor[i][0])*abs(Spinor[i][0])+abs(Spinor[i][1])*abs(Spinor[i][1])
        module.append(Module)
    
    return module



#Trans a spinor or a bunch of spinors that average in vertical direction to (theta,phi)
def TransferToN(Spinor,theta,phi):
    Len=len(Spinor)
    u11=cmath.exp(-1j*phi/2)*math.cos(theta/2)   #Positive or negative sign is realated to direction of the transform
    #u11=cmath.exp(1j*phi/2)*math.cos(theta/2) 
    u12=-1*cmath.exp(-1j*phi/2)*math.sin(theta/2)
    #u12=cmath.exp(-1j*phi/2)*math.sin(theta/2)
    u21=cmath.exp(1j*phi/2)*math.sin(theta/2)
    #u21=-1*cmath.exp(1j*phi/2)*math.sin(theta/2)
    u22=cmath.exp(1j*phi/2)*math.cos(theta/2)
    #u22=cmath.exp(-1j*phi/2)*math.cos(theta/2)
    for i in range(Len):
        a=Spinor[i][0]
        Spinor[i][0]=u11*Spinor[i][0]+u12*Spinor[i][1]
        Spinor[i][1]=u21*a+u22*Spinor[i][1]


    return



def CalSx(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag

        #spinXup=(Spinor[i][0]+Spinor[i][1])/math.sqrt(2)
        #spinXdown=(Spinor[i][0]-Spinor[i][1])/math.sqrt(2)
        #sigmai=abs(spinXup)*abs(spinXup)-abs(spinXdown)*abs(spinXdown)
        #Verified program to calculate Polarization degree
        sigmai=UCon*Spinor[i][1]+DCon*Spinor[i][0]
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S1 not real, S1= \033[0m',sigmai)
        sigma.append(sigmai.real)
    #sum=0
    #for i in sigma:
    #    sum=sum+i
        
    #Pordegree=sum/Length
  

    return sigma

def CalSxAverage(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        #spinXup=(Spinor[i][0]+Spinor[i][1])/math.sqrt(2)
        #spinXdown=(Spinor[i][0]-Spinor[i][1])/math.sqrt(2)
        #sigmai=abs(spinXup)*abs(spinXup)
        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag        
        sigmai=UCon*Spinor[i][1]+DCon*Spinor[i][0]
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S1 not real, S1= \033[0m',sigmai)

        sigma.append(sigmai.real)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/Length
  

    return Pordegree


def CalSxAverage_Intrinsic_Phase(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):

        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag        
        sigmai=(UCon*Spinor[i][1]+DCon*Spinor[i][0])*0.5*math.exp((-1*Spinor[i][2])/2)
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S1 not real, S1= \033[0m',sigmai)

        sigma.append(sigmai.real)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/8
  

    return Pordegree

def CalSxAverage_Intrinsic(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):

        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag        
        sigmai=(UCon*Spinor[i][1]+DCon*Spinor[i][0])*0.5*math.exp((-1*Spinor[i][2])/2)
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S1 not real, S1= \033[0m',sigmai)

        sigma.append(sigmai.real)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum
  

    return Pordegree


def CalSs(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag
        

        sigmai=-1j*(UCon*Spinor[i][1]-DCon*Spinor[i][0])
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S2 not real, S2= \033[0m',sigmai)
        sigma.append(sigmai.real)

  
    return sigma

def CalSsAverage(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):

        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag
        sigmai=-1j*(UCon*Spinor[i][1]-DCon*Spinor[i][0])
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S2 not real, S2= \033[0m',sigmai)
        sigma.append(sigmai.real)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/Length
  

    return Pordegree


def CalSsAverage_Intrinsic_Phase(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):

        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag
        sigmai=-1j*(UCon*Spinor[i][1]-DCon*Spinor[i][0])*0.5*math.exp((-1*Spinor[i][2])/2)
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S2 not real, S2= \033[0m',sigmai)
        sigma.append(sigmai.real)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/8
  

    return Pordegree

def CalSsAverage_Intrinsic(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):

        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag
        sigmai=-1j*(UCon*Spinor[i][1]-DCon*Spinor[i][0])*0.5*math.exp((-1*Spinor[i][2])/2)
        if(sigmai.imag>0.0001):
            print('\033[4;31;43mERROR: S2 not real, S2= \033[0m',sigmai)
        sigma.append(sigmai.real)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum
  

    return Pordegree

def CalDirectionofSpinor(Spinor):     #2 angle varibles can describe a direction ,theta from 0 to pi ,phi from 0 to 2pi,
    Length=len(Spinor)                #for phi,it is neccessary to use both S1 and S2 to verify wheather phi locates on 0 to pi or pi to 2pi
    Direction=[]
    S1=CalSx(Spinor)
    S3=CalSy(Spinor)
    S2=CalSs(Spinor)
    for i in range(Length):

        try:
            theta=math.acos(S3[i])
        except ValueError:
            if(S3[i]>0):
                theta=0
                print('ValveError Happens,theta is set to 0 ;S3=',S3[i])
            else:
                theta=3.1415926535898
                print('ValveError Happens,theta is set to pi ;S3=',S3[i])


        
        if(theta==0 or theta==3.1415926535898):
            phi='non'
        else:
            if(S2[i]>=0):

                if((S1[i]/math.sin(theta))>=1.):
                    phi=math.acos((S1[i]/math.sin(theta))-0.0000000000001)   #To avoid math domain error
                elif((S1[i]/math.sin(theta))<=1.):
                    phi=math.acos((S1[i]/math.sin(theta))+0.0000000000001) 
                else:
                    phi=math.acos(S1[i]/math.sin(theta))              
            else:
                if((S1[i]/math.sin(theta))>=1.):
                    phi=2*math.pi-math.acos((S1[i]/math.sin(theta))-0.0000000000001)   
                elif((S1[i]/math.sin(theta))<=-1.):
                    phi=2*math.pi-math.acos((S1[i]/math.sin(theta))+0.0000000000001) 
                else:
                    phi=2*math.pi-math.acos(S1[i]/math.sin(theta))
        Direction.append([theta,phi])
    return Direction

def GeneratePartialSnakeSpin(SnakeStrengthphi,GGamma):  #Generate a Spinor on direction of n0 with a partial snake ,partial snake is on e2 direction
    cc=math.cos(math.pi*GGamma)*math.cos(SnakeStrengthphi/2)
    pivues=math.acos(cc)
    cosalpha1=0.
    cosalpha2=math.sin(SnakeStrengthphi/2)/math.sin(pivues)
    cosalpha3=(math.sin(math.pi*GGamma)*math.cos(SnakeStrengthphi/2))/math.sin(pivues)
    S1=cosalpha1
    S2=cosalpha2
    S3=cosalpha3
    theta=math.acos(S3)
    if(S2>=0):
        phi=math.acos(S1/math.sin(theta))
    else:
        phi=2*math.pi-math.acos(S1/math.sin(theta))
    
    Spinor=[]
    Spinor.append([complex(math.cos(theta/2)),math.sin(theta/2)*cmath.exp(1j*phi)])

    #Spinor[0][0]=complex(math.cos(theta/2))
    #Spinor[0][1]=math.sin(theta/2)*cmath.exp(1j*phi)

    return Spinor

#Calculate the polarization degree on (theta phi) direction , An assist spinor is used to calculate S_i which is useful
def CalSn(Spinor,theta,phi):
    AssSpinor=GenerateSpin(phi,theta)
    S1=CalSxAverage(AssSpinor)
    S2=CalSsAverage(AssSpinor)
    S3=CalSyAverage(AssSpinor)
    S11=S3
    S12=S1-1j*S2
    S21=S1+1j*S2
    S22=-S3

    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag
        sigmai=UCon*(S11*Spinor[i][0]+S12*Spinor[i][1])+DCon*(S21*Spinor[i][0]+S22*Spinor[i][1])
        if(sigmai.imag>0.00000001):
            print('\033[4;31;43mERROR: Sn not real, Sn= \033[0m',sigmai)
        sigma.append(sigmai.real)

    return sigma

def CalPolarizationDegree(Spinor):
    Sx=CalSxAverage(Spinor)
    Ss=CalSsAverage(Spinor)
    Sy=CalSyAverage(Spinor)
    P=Sx*Sx+Sy*Sy+Ss*Ss

    return P

    