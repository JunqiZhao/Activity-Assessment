import pandas as pd
import numpy as np
from numpy import genfromtxt
import os
import datetime
from time import sleep
os.chdir('D:\\Academic\\Research Works\\Activity Evaluation and DSS\Code')
# Load Activities Result from csv as numpy array
act=genfromtxt('S1_Y_Trial (1-6).csv', delimiter=',')
# Define Threshold for Activities
threshold= np.array([10,10,10,10,10,10]) # Safety Threshold in seconds
lab_names= np.array(["BT","KN","LB","OW","ST","WK"])
columns=['Activities','Count of MHT','Total Duration of MHT','Frequency of Exposture in 1 Minute','Proportion of Activities','Max MHT']
index=range(6)
result = pd.DataFrame(index=index,columns=columns)
result.iloc[:,0]=lab_names
result = result.fillna(0) # with 0s rather than NaNs
def quasiEVA(lable_array,threshold,result):
    j=0
    c=len(np.unique(lable_array))
    rows=len(lable_array)
    count=np.zeros(shape=(rows,2))
    #count sliding windows for each activities
    for i in range(rows-1):
        if lable_array[i+1]==lable_array[i]:
            count[j,1]+=1
            count[j,0]=lable_array[i]
        else:
            j+=1
            count[j,0]=lable_array[i]
            count[j,1]+=1
    #count holding time
    HT=count.sum(1)[...,None] # None keeps (n, 1) shape
    HT[:,0]=0
    HT[:,0]=(count[:,1]+1)*0.5
    count=np.append(count,HT,1)
    ##activities' MHT
    for i in range(c):
        count_red=count
        count_red=count[count[:,0]==i+1]
        count_red_result=count_red[count_red[:,1]>threshold[i]] # filtering out all the MHT above threshold
        result.iloc[[i],[1]]=len(count_red_result[:,1]) #total count of breaching MHT
        result.iloc[[i],[2]]=sum(count_red_result[:,1]) #total duration of breaching MHT
        result.iloc[[i],[3]]=len(count_red_result[:,1])/sum(count[:,2])*60 #frequencies of activity i occurance in 1 minute
        result.iloc[[i],[4]]=sum(count_red[:,1])/sum(count[:,1]) #proportion of activity i
        result.iloc[[i],[5]]=max(count_red_result[:,1]) #max time of holding
    return result
# Get the Quasi-Realtime Evaluation Result
eva_result=quasiEVA(act,threshold,result)


# Get Real-time Evaluation Result
def realEVA(lable_array,threshold):
    timer=0
    thresh=0
    for i in range(len(lable_array)-1):
        sleep(0.1) #control the rate of running the program
        a1=int(lable_array[i])
        a2=int(lable_array[i+1])
        if a1==a2:
            timer+=1
            thresh=threshold[a1-1] #find the corresponding threshold
            if 0.5*(timer+1)>thresh: #convert count to actual safety threshold seconds
                timer=0 # for now, we only consider the first time when the threshold was breached, then reset the timer at zero
                print("MHT of "+lab_names[a1-1]+" exceeds the safety threshold at "+str(i)+" and "+str(datetime.datetime.now()))
        else:
            timer=0
# Get the Realtime Evaluation Result
realEVA(act,threshold)
