# -*- coding: utf-8 -*-
"""
Created on Thu Feb 12 18:27:26 2026

@author: Pradeep
"""

import pyperclip
path = pyperclip.paste()
path = path.strip('"')

os.chdir(path)
fileList = os.listdir(path)
h5Files = []

for i in fileList:
    if i.endswith('h5'):
        h5Files = np.append(h5Files,i)
df = pd.DataFrame (h5Files, columns = ['Files_in_Folder'])
fileList = h5Files
print(df)

from scipy.signal import medfilt, savgol_filter
finalUnwindingLength = []
finalPauseDuration = []
for k in np.arange(0, len(fileList)):
    
    file = lk.File(fileList[k])
    dist1 = file.distance1.data
    dist1 = ((dist1-6.07)/(12.06-6.07))*17853 #converting to nt unwound
    dist1 = dist1-dist1[0]
    #f1x_timestamps = file.force1x.timestaC:\Users\prade\Dropbox (HMS)\Data\C-trap\2023\sPS42a_haloUb-gfp-MBP_tethered_Repeatmps # This is plotting actual time stamp from machine
    time = file.distance1.seconds # This is for plotting time in seconds
    if time[-1] > 60:
        # smoothed = medfilt(dist1, kernel_size=45)
        smoothed2 = savgol_filter(dist1, window_length=51, polyorder=2)

        # dt = np.diff(time)  # Assuming time is equally spaced
        # dy = np.diff(smoothed2)
        # slope = dy / dt  # Instantaneous ratecx
        # Pad to match lengths
        # slope = np.concatenate([[0], slope])
        #getting unwinding length for the nearest time
        target_t = 60 
        idx60 = np.argmin(np.abs(time - target_t))
        unwound_at_60 = smoothed2[idx60]        
        finalUnwindingLength = np.append(finalUnwindingLength, unwound_at_60)
        #assessingPauseDuration until the time specified
        trim_dist = smoothed2[0:idx60]
        trim_time = time[0:idx60]
        
        dt = np.diff(trim_time)  # Assuming time is equally spaced
        dy = np.diff(trim_dist)
        slope = dy / dt  # Instantaneous ratecx
        # Pad to match lengths
        slope = np.concatenate([[0], slope])

        flat_threshold = 2.0  # nt/s, adjust as needed
        is_flat = np.abs(slope) < flat_threshold

        distFlat = dist1[is_flat]
        timeFlat= time[is_flat]
        tempPauseDuration = round(sum(is_flat)/len(is_flat) * 100, 2)
        finalPauseDuration = np.append(finalPauseDuration, tempPauseDuration)
        plt.plot(time,smoothed2, color='black' )
        plt.scatter(timeFlat, distFlat, color='yellow', edgecolors='none', s=50, alpha=0.6, marker='o')
        print('The fraction of trace that is paused is ',round(sum(is_flat)/len(is_flat) * 100, 2), '%')

    
