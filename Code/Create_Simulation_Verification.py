##DATA CLEANING FILE##
import csv
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

#Read csv file.
df = pd.read_csv(r"C:\Users\Logan\Desktop\School Files\Senior Project\Shared_Dat\PhaseII_ET_WithNextWater.csv")
df2 = pd.read_csv(r"C:\Users\Logan\Desktop\School Files\Senior Project\Shared_Dat\Depricated_data\ET_FIXED_DATE.csv")

#Convert date to datetime objects, add two new columns
df['Date'] = pd.to_datetime(df.Date, format='%m/%d/%y')
df2['Date'] = pd.to_datetime(df2.Date, format='%m/%d/%y')
df['nextET1'] = 0.0
df['nextRain1'] = 0.0
df['nextET2'] = 0.0
df['nextRain2'] = 0.0
df['nextET3'] = 0.0
df['nextRain3'] = 0.0
df['nextET4'] = 0.0
df['nextRain4'] = 0.0
df['nextET5'] = 0.0
df['nextRain5'] = 0.0

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
        
        tempDay = dates[j]
        rainVals = [0.0, 0.0, 0.0, 0.0, 0.0]
        eVals = [0.0, 0.0, 0.0, 0.0, 0.0]
        for k in range(datediff):
            tempDay += pd.DateOffset(days = 1)
            rainVal = df2.loc[(df2['Date'] == tempDay), 'Rainfall'].item()
            eVal = - df2.loc[(df2['Date'] == tempDay), 'ETRef'].item()

            rainVals[k] = rainVal
            eVals[k] = eVal

        # Assign the new list to the DataFrame column
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextRain1'] = rainVals[0]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextET1'] = eVals[0]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextRain2'] = rainVals[1]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextET2'] = eVals[1]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextRain3'] = rainVals[2]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextET3'] = eVals[2]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextRain4'] = rainVals[3]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextET4'] = eVals[3]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextRain5'] = rainVals[4]
        df.loc[(df['Plot.No'] == i) & (df['Date'] == dates[j]), 'nextET5'] = eVals[4]

df.to_csv(r"C:\Users\Logan\Desktop\School Files\Senior Project\Shared_Dat\PhaseII_ET_WithNextWater.csv", index = False) #save
