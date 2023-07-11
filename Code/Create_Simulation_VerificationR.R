library(readr)
library(dplyr)
library(lubridate)

#Read csv file.
df <- read_csv("C:/Users/Logan/Desktop/School Files/Senior Project/Shared_Dat/PhaseII_ET_WithNextWater.csv")
df2 <- read_csv("C:/Users/Logan/Desktop/School Files/Senior Project/Shared_Dat/Depricated_data/ET_FIXED_DATE.csv")

#Convert date to datetime objects, add two new columns
df$Date <- mdy(df$Date)
df2$Date <- mdy(df2$Date)

df$nextET1 <- 0.0
df$nextRain1 <- 0.0
df$nextET2 <- 0.0
df$nextRain2 <- 0.0
df$nextET3 <- 0.0
df$nextRain3 <- 0.0
df$nextET4 <- 0.0
df$nextRain4 <- 0.0
df$nextET5 <- 0.0
df$nextRain5 <- 0.0

#Iterate through all unique plots
for (i in unique(df$`Plot.No`)){
  sample <- df[df$`Plot.No` == i,]
  dates <- unique(sample$Date) #Get all unique dates for a given plot
  
  #Iterate through all unique dates minus 1
  for (j in 1:(length(unique(sample$Date))-1)){
    #Find next observation, find number of days, update observation columns.
    datediff <- as.integer(abs(difftime(dates[j], dates[j+1], units = "days")))
    
    tempDay <- dates[j]
    rainVals <- c(0.0, 0.0, 0.0, 0.0, 0.0)
    eVals <- c(0.0, 0.0, 0.0, 0.0, 0.0)
    
    for (k in 1:datediff){
      tempDay <- tempDay + days(1)
      rainVal <- df2$Rainfall[df2$Date == tempDay]
      eVal <- -df2$ETRef[df2$Date == tempDay]
      
      rainVals[k] <- rainVal
      eVals[k] <- eVal
    }
    
    # Assign the new list to the DataFrame column
    thisIndex <- which(df$`Plot.No` == i & df$Date == dates[j])
    df$nextRain1[thisIndex] <- rainVals[1]
    df$nextET1[thisIndex] <- eVals[1]
    df$nextRain2[thisIndex] <- rainVals[2]
    df$nextET2[thisIndex] <- eVals[2]
    df$nextRain3[thisIndex] <- rainVals[3]
    df$nextET3[thisIndex] <- eVals[3]
    df$nextRain4[thisIndex] <- rainVals[4]
    df$nextET4[thisIndex] <- eVals[4]
    df$nextRain5[thisIndex] <- rainVals[5]
    df$nextET5[thisIndex] <- eVals[5]
  }
}

write_csv(df, "C:/Users/Logan/Desktop/School Files/Senior Project/Shared_Dat/SIM_VERIFY2.csv") #save

