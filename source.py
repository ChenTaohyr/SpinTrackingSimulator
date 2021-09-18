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

    print('Initial Spinor',Spinor)
    #print 'Initialization done'
    
    return Spinor

#For a specified porlaration degree,all particles are assign to the same up and down compnents -
#-and a  random phase factor 
def InitializeRandomPhase(InitialPolarizationDegree,ParticleNum):
    #print 'Initializing...'
    #print('InitialPolarizationDegree ' ,InitialPolarizationDegree)
    #print('particlenum ' ,ParticleNum)

    Spinor=[]
    for i in range(ParticleNum):
        RandomPhase1=2j*random.random()*math.pi
        RandomPhase2=2j*random.random()*math.pi
        RandomPhase3=2j*random.random()*math.pi
        up=math.sqrt((InitialPolarizationDegree+1)/2)
        down=math.sqrt((1-InitialPolarizationDegree)/2)
        #Spinor.append([up*cmath.exp(RandomPhase1),down*cmath.exp(RandomPhase2)])
        Spinor.append([up*cmath.exp(RandomPhase1)*cmath.exp(RandomPhase3),down*cmath.exp(RandomPhase3)])    #another approach to generate random phase spinor
           
    print('Initial Spinor',Spinor)
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
def PartialResonanceKick(Spinor,GGamma,K,eplison,thetai,thetaf):
    #eplison=GGamma*0.002
    delta=K-GGamma
    lamda=math.sqrt(delta*delta+abs(eplison)*abs(eplison))
    b=(abs(eplison)*math.sin(lamda*(thetaf-thetai)/2))/lamda
    a=math.sqrt(1-b*b)
    
    #if (lamda-int(lamda)>0.5):       #Fix the error that arctan(Tan(x)) may lost some phase of a (integer*pi)
    #    AngleNum=int(lamda+1)
    #else:
    #    AngleNum=int(lamda)     

    #Fix Error :The above code is only correct for 2 pi arc
    #phaseNum=lamda*(thetaf-thetai)/(2*math.pi)
    #if (phaseNum-int(phaseNum)>0.5):       #Fix the error that arctan(Tan(x)) may lost some phase of a (integer*pi)
    #    AngleNum=int(phaseNum)+1
    #else:
    #    AngleNum=int(phaseNum)


    #The above 2 phase are all wrong

    cos_phi=math.cos(lamda*(thetaf-thetai)/2)
    if (cos_phi>=0):
        AngleNum=0

    else:
        AngleNum=1
    

    c=math.atan((delta*math.tan(lamda*(thetaf-thetai)/2))/lamda)+AngleNum*math.pi
    #c=math.atan((delta*math.tan(lamda*(thetaf-thetai)/2))/lamda)
    d=-1*cmath.phase(eplison)
    #print(c,delta)
    Length=len(Spinor)
    for i in range(Length):
        
        x=Spinor[i][0]
        Spinor[i][0]=Spinor[i][0]*a*cmath.exp((c-K*(thetaf-thetai)/2)*1j)+1j*b*Spinor[i][1]*cmath.exp(-1j*(d+K*(thetaf+thetai)/2))
        Spinor[i][1]=x*(1j)*b*cmath.exp(1j*(d+K*(thetaf+thetai)/2))+Spinor[i][1]*a*cmath.exp(-1j*(c-K*(thetaf-thetai)/2))
       

    return


#Calculate polarization degree
#polarization degree=<<Sigma3>>
def CalPorDegree(Spinor):
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


def CalPorDegreeOneByOne(Spinor):
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

#Trans a spinor to the horizonal plane
##For benchmark of the snakes .It can transfer (1,0) to the direction "that not change under snakes".
#Only for single particle ,invariant GGamma,for snake direction phis=0.
def TransferToN(Spinor,GGamma):
    AngleWithN=-1j*(1-(GGamma-int(GGamma))*math.pi)
    #AngleWithN=1
    a=Spinor[0][0]
    Spinor[0][0]=(1/math.sqrt(2))*(Spinor[0][0]*cmath.exp(AngleWithN)+Spinor[0][1]*-1*cmath.exp(-AngleWithN))
    Spinor[0][1]=(1/math.sqrt(2))*(a*cmath.exp(AngleWithN)+Spinor[0][1]*cmath.exp(-AngleWithN))

    return



def CalPorDegreeX(Spinor):
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
            print('ERROR: S1 not real S1=',sigmai)
        sigma.append(sigmai.real)
    #sum=0
    #for i in sigma:
    #    sum=sum+i
        
    #Pordegree=sum/Length
  

    return sigma

def CalPorX(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        spinXup=(Spinor[i][0]+Spinor[i][1])/math.sqrt(2)
        spinXdown=(Spinor[i][0]-Spinor[i][1])/math.sqrt(2)
        sigmai=abs(spinXup)*abs(spinXup)
        sigma.append(sigmai)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/Length
  

    return Pordegree


def CalPorDegreeY(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        UCon=Spinor[i][0].real-1j*Spinor[i][0].imag
        DCon=Spinor[i][1].real-1j*Spinor[i][1].imag
        
        #spinYup=((Spinor[i][0]-1j*Spinor[i][1])*math.sqrt(2))/2
        #spinYdown=((Spinor[i][0]+1j*Spinor[i][1])*math.sqrt(2))/2
        #sigmai=abs(spinYup)*abs(spinYup)-abs(spinYdown)*abs(spinYdown)
        sigmai=-1j*(UCon*Spinor[i][1]-DCon*Spinor[i][0])
        if(sigmai.imag>0.0001):
            print('ERROR: S2 not real, S2= ',sigmai)
        sigma.append(sigmai.real)
    #sum=0
    #for i in sigma:
    #    sum=sum+i
        
    #Pordegree=sigma
  
    return sigma

def CalPorY(Spinor):
    sigma=[]
    Length=len(Spinor)
    for i in range(Length):
        spinYup=((Spinor[i][0]-1j*Spinor[i][1])*math.sqrt(2))/2
        spinYdown=((Spinor[i][0]+1j*Spinor[i][1])*math.sqrt(2))/2
        sigmai=abs(spinYup)*abs(spinYup)
        sigma.append(sigmai)
    sum=0
    for i in sigma:
        sum=sum+i
        
    Pordegree=sum/Length
  

    return Pordegree

def CalDirectionofSpinor(Spinor):     #2 angle varibles can describe a direction ,theta from 0 to pi ,phi from 0 to 2pi,
    Length=len(Spinor)                #for phi,it is neccessary to use both S1 and S2 to verify wheather phi locates on 0 to pi or pi to 2pi
    Direction=[]
    S1=CalPorDegreeX(Spinor)
    S3=CalPorDegreeOneByOne(Spinor)
    S2=CalPorDegreeY(Spinor)
    for i in range(Length):
        #S1=CalPorDegreeX(Spinor)
        #S3=CalPorDegree(Spinor)
        #S2=CalPorDegreeY(Spinor)
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
                
                phi=math.acos((S1[i]/math.sin(theta))-0.0000000000001)   #To avoid math domain error
            else:
                
                phi=2*math.pi-math.acos((S1[i]/math.sin(theta))-0.0000000000001)
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


def Cal0_3PolarizationDegree(Spinor):
    #Length=len(Spinor)
    #for i in range(Length):
    S3=CalPorDegreeOneByOne(Spinor)[0]
    S2=CalPorDegreeX(Spinor)[0]
    theta=CalDirectionofSpinor(Spinor)[0][0]
    print('theta= ',theta)
    S_Direction=S3*math.cos(theta)+S2*math.sin(theta)
    return S_Direction
    