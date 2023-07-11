##DATA CLEANING FILE##
##This script is used to add two new columns containing the next VWC observation within the data.
## This allows for comparison of the current VWC value to it's next observed value.

##This program works by reading in the data with pandas, creates two new columns,
## then iterating through all unique plots & dates, setting the next observation as the following date.

##NOTE: Script assumes data is pre-sorted by date oldest-newest.

import csv
import pandas as pd
from datetime import datetime 
import numpy as np

#Read csv file.
df = pd.read_csv(r"C:\Users\Logan\Desktop\School Files\Senior Project\Shared_Dat\PhaseII_ET.csv")
#Convert date to datetime objects, add two new columns
df['Date'] = pd.to_datetime(df.Date, format='%m/%d/%y')
df['nextVWC_Observation'] = 0.0
df['daysUntilNextObservation'] = 0
df['CWB'] = 0.0
df['NonZeroRain'] = False
df['CRain'] = 0.0
df['CET'] = 0.0
df['CIrr'] = 0.0

#Iterate through all unique plots
for i in df['Plot.No'].unique():
    sample = df[df['Plot.No'] == i]
    dates = sample['Date'].unique() #Get all unique dates for a given plot
    
    #Iterate through all unique dates minus 1
    for j in range(len(sample['Date'].unique())-1):
        #Find next observation, find number of days, update observation columns.
        datediff = dates[j] - dates[j+1]
        datediff = datediff.astype('timedelta64[D]')
        datediff = abs(int(datediff / np.timedelta64(1, 'D')))
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextVWC_Observation'] = df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j+1]), 'Mean.VWC'].item()
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'daysUntilNextObservation'] = datediff
        
        thisWater = df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'CumNet'].item()
        nextWater = df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j+1]), 'CumNet'].item()
        diff = nextWater - thisWater
        diffCopy = nextWater - thisWater
        if df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'Irrigated.After'].item() == "Yes":
            diff = diff + 0.25
            df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'CIrr'] = 0.25
        
        thisRain = df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'CumulativeRainfall'].item()
        nextRain = df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j+1]), 'CumulativeRainfall'].item()
        if (nextRain - thisRain > 0):
            df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'NonZeroRain'] = True

        
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'CRain'] = (nextRain - thisRain)
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'CWB'] = diff
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'CET'] = diffCopy - (nextRain - thisRain)
df.to_csv(r"C:\Users\Logan\Desktop\School Files\Senior Project\Shared_Dat\PhaseII_ET_TEST.csv", index = False) #save
