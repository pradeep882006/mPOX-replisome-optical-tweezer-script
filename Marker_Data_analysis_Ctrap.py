# -*- coding: utf-8 -*-
"""
Created on Sat May 24 15:51:36 2025

@author: prade
analysis for HSV polymerase activity on lumicks DNA substrate
For conversion used Bustamante fomula

"""
import numpy as np
import matplotlib.pyplot as plt
import os
import lumicks.pylake as lk
import pandas as pd
%matplotlib auto

#%%
# GEtting the file list from the folder 
# path = r'C:\Users\prade\Dropbox (HMS)\Data\C-trap\2023\PulledOnHaloNewCdc48_Halo-Ub-MBP-GFP-Spytag'
os.chdir(path)
fileList = os.listdir(path)
h5Files = []

for i in fileList:
    if i.endswith('h5'):
        h5Files = np.append(h5Files,i)
df = pd.DataFrame (h5Files, columns = ['Files_in_Folder'])
fileList = h5Files
print(df)


#%%
# GEtting the file list from the folder 
# path = r'C:\Users\prade\Dropbox (HMS)\Data\C-trap\2023\PulledOnHaloNewCdc48_Halo-Ub-MBP-GFP-Spytag'
os.chdir(path)
fileList = os.listdir(path)
h5Files = []

for i in fileList:
    if i.endswith('h5'):
        h5Files = np.append(h5Files,i)
df = pd.DataFrame (h5Files, columns = ['Files_in_Folder'])
fileList = h5Files
print(df)

#%% Selecting file number
k = 1

file = lk.File(fileList[k])

#file = lk.File(fileList[8])
#file.force1x.plot() # for plotting the force quickly
#For extracting the force1x and plotting the data against the time (not distance because there is no FD).
dist1 = file.distance1.data
dist1 = ((dist1-6.07)/(12.06-6.07))*17853
dist1 = dist1-dist1[0]
#f1x_timestamps = file.force1x.timestaC:\Users\prade\Dropbox (HMS)\Data\C-trap\2023\sPS42a_haloUb-gfp-MBP_tethered_Repeatmps # This is plotting actual time stamp from machine
time = file.distance1.seconds # This is for plotting time in seconds
fig, axs = plt.subplots(figsize=(8,6))
plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)
axs.set_xlabel('Time (s)', fontsize = 18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
for spine in axs.spines.values():
    spine.set_linewidth(1.25)
axs.tick_params(width=1.25)
axs.set_ylabel('Distance (nt)',fontsize = 18)
axs.plot(time, dist1) #Final plot after extracting the data in previous statemnts

# plt.savefig(str(fileList[k][:-3])+"DistanceData", dpi = 600)
# plt.tight_layout()
#plt.savefig("Force1x.pdf", format="pdf")
# fig.set_size_inches(5, 3)
#axs.set_ylim(np.min(dist1), np.max(dist1))
#plt.savefig(fileList[k][:-3]+'Dist1'+'.pdf', format="pdf", bbox_inches = 'tight')

#%% Saving multiple file sin folder

for k in np.arange(0,len(fileList)):
       
    file = lk.File(fileList[k])
    
    #file = lk.File(fileList[8])
    #file.force1x.plot() # for plotting the force quickly
    #For extracting the force1x and plotting the data against the time (not distance because there is no FD).
    dist1 = file.distance1.data
    dist1 = ((dist1-6.07)/(12.06-6.07))*17853
    dist1 = dist1-dist1[0]
    #f1x_timestamps = file.force1x.timestaC:\Users\prade\Dropbox (HMS)\Data\C-trap\2023\sPS42a_haloUb-gfp-MBP_tethered_Repeatmps # This is plotting actual time stamp from machine
    time = file.distance1.seconds # This is for plotting time in seconds
    fig, axs = plt.subplots(figsize=(8,6))
    plt.subplots_adjust(left=0.2, right=0.9, top=0.9, bottom=0.2)
    axs.set_xlabel('Time (s)', fontsize = 18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    for spine in axs.spines.values():
        spine.set_linewidth(1.25)
    axs.tick_params(width=1.25)
    axs.set_ylim([-50,500])
    axs.set_ylabel('Distance (nt)',fontsize = 18)
    axs.plot(time, dist1) #Final plot after extracting the data in previous statemnts
    plt.savefig(str(fileList[k][:-3])+"Dist.pdf", dpi = 600)
