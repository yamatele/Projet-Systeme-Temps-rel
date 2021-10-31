#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 10:55:47 2021

@author: ndo
"""
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import math as m
import itertools as ite
from operator import itemgetter

class Task:
    def __init__(self):
        print("please enter the following values for your task :")
        print("Cost , deadline and period :")
        self.cost,self.deadLine,self.period = map(int, input().split())
        #self.cost= int(input("The cost:  "))
        #self.period=int(input("The period:  "))
        #self.deadLine= int(input("The deadLine:  "))
        self.CT= self.cost/self.period
        self.CD= self.cost/self.deadLine
        
        self.done=False
        self.did=0
        
        
        
        
        
    def getCost(self):
            return self.cost
        
        
    def getPeriod(self):
            return self.period
        
    def getDeadL(self):
            return self.deadLine
        
    def setCost(self,cost):
              self.cost=cost
              
    def setPeriod(self,period):
              self.period=period
              
    def setDeadL(self,deadLine):
              self.deadLine=deadLine
    def getTask(self):
        Ta=[self.cost,self.deadLine,self.period]
        return Ta
    #def printTask():
        #print(self.cost, self.deadLine,self.period)
        

########################################

class Scheduler:
    
    
    def __init__(self):
        self.jobs=[]##jobs tha we are going to work with
        self.newJobs=[]#jobs that migt be added
        self.Okayjobs=[]##validated jobs
        self.load=0#processor load
        
      
        self.Maxload=1 #max load of processor
        self.n=0 #number of tasks in jobs
        self.nLoaded=0 #number of tasks loaded
        self.NC=True #necessary condition
        self.NSC=True#necessary and sufficient condition
        
        self.lcm=0
        self.Busyperiod=0
        self.responseTime=[]
        self.simLength=[]
        self.error=0
        
        
        
    #we are going to create our first set of tasks
    def MyFirstTasks(self,n):
        
        self.n=n
        self.nLoaded=n
        
        for i in range(0,self.n):
            self.newJobs.append(Task())
        self.jobs+=self.newJobs #we add them to the jobs
        
        
        
    def AddTasks(self,n):
        
        self.newJobs=[]
        self.nLoaded=0
        self.nLoaded=n
        self.n+=n
        
        for i in range(0,n):
            
            self.newJobs.append(Task()) 
            self.jobs+=self.newJobs
            #we add them to the jobs
            
    
    def N_and_S_Cond_EDF(self): ##necessary and sufficient condition for EDF
        self.load =0
        self.NSC= True
        for i in range(0,self.n):
            self.load += self.jobs[i].CT
            
        if self.load>self.Maxload: 
            self.NSC= False
            self.n-=self.nLoaded
            del self.jobs[len(self.jobs)-self.nLoaded-1 : len(self.jobs) ]
            
            
            
    def N_Cond_DM(self): 
        self.load =0
        self.NC= True
        inv= 1/self.n
        for i in range(0,self.n):
            self.load += self.jobs[i].CD
        if self.load>self.n*(m.pow(2,inv)-1):
            self.NC= False
        
            
        
        
        
    def Busy_period(self):
        summ=0
        W=[]
        Find = True
        up=0
        for i in range(0, self.n):
            summ+= self.jobs[i].cost
        W.append(summ)

        while Find==True :
            summ=0
            for i in range(0, self.n):
                up= W[-1]/self.jobs[i].period
                summ+= m.ceil(up)*self.jobs[i].cost   
            W.append(summ)
            
            if (W[-2]==W[-1]):
                Find=False
            
            
        self.Busyperiod=W[-1]
        
        
        
        
        
    def PPCM(self):
        tamp = self.jobs[0].period
        for i in range(1,self.n) :
           tamp = np.lcm(tamp,self.jobs[i].period)  
        self.lcm=tamp
        self.simLength = list(ite.repeat(0,tamp))
        print(*self.simLength)
    
   
    
    def printTasks(self):
        for i in range(0,self.n):
            print(*self.jobs[i].getTask())
            
            
            
   ############################Scheduling algorithms#################################
    def sorting(self):
        oup=[]
        Work=[0]*self.n
        for i in range(0, self.n):
            oup.append(self.jobs[i].getTask())
        sorted(oup,key=itemgetter(1))
        for j in range(0, self.n):
            
            for k in range(0,self.n):
                if self.jobs[j].deadLine == oup[k][2] :
                    Work[k]=self.jobs[j]
        self.jobs=Work        
                
     
    def DM_Scheduling(self):
     self.error =0   
     cursor=0  
     p_counter=0##counter of period
     d_counter=0## deadline counter
      
     
     for i in range(0,len(self.jobs)):
         d_counter=self.jobs[i].deadLine
         #p_counter=self.jobs[i].period
         p_counter=0
         
         for j in range(0,len(self.simLength)):
             
            if self.simLength[j]==0 and self.jobs[i].did< self.jobs[i].cost :
                self.simLength[j]=1
                self.jobs[i].did+=1
                
            if (self.jobs[i].did==self.jobs[i].cost and d_counter>=0) :
                self.jobs[i].done = True
                d_counter=self.jobs[i].deadLine
                
            
            if self.jobs[i].period==p_counter and self.jobs[i].done is True:
                p_counter=0
                self.jobs[i].did=0
                self.jobs[i].done = False
            else :
                 p_counter+=1
            
                
                
                
            if self.jobs[i].done==False and d_counter<=0: 
                 cursor = j+1
                 self.error = cursor
                 return 2
                
               
            if self.jobs[i].done is False :
                d_counter-=1
            
     return 1      
                 
                 
             
            
            
       


if __name__=='__main__':
    
    sche= Scheduler()
    sche.MyFirstTasks(2)
    
    sche.N_and_S_Cond_EDF()
    sche.N_Cond_DM()
    
    print(sche.load)
    if sche.NC is True :
        print("Deadline monotonic can be applied")
    else :
        print("Deadline monotonic necessary condition isn't met yet")
    if sche.NSC is True: 
        print("Success processor not overloaded")
    else :
      print("failed, processor overloaded")
     
    print("Tasks in Job")
    print(sche.printTasks(),sep=("\n"))
    print("tasks loaded recently")
    #print("\n".join(map(str,sche.newJobs)))
    
    a=int(input("Rajoutez des taches, vous voulez en rajouter combien?:  "))
    
    sche.AddTasks(a)
    
    #print("\n".join(map(str,sche.jobs)))
    #print("\n".join(map(str,sche.jobs)))
    sche.Busy_period()
    print("Busy period is equal to ")
    print(sche.Busyperiod)
    sche.PPCM()
    print(sche.lcm)
    sche.N_and_S_Cond_EDF()
    sche.N_Cond_DM()
    sche.sorting()
    print(sche.printTasks(),sep=("\n"))
    print("DM scheduling for the tasks :") 
    abo=sche.DM_Scheduling()
    if abo==1:
        print("Okay")
    else :
        print("Not okay at")
        print(sche.error)        
            