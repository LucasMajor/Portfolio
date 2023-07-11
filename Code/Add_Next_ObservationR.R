library(readr)
library(dplyr)
library(lubridate)

#Read csv file.
df <- read_csv("C:/Users/Logan/Desktop/School Files/Senior Project/Shared_Dat/PhaseII_ET.csv")

#Convert date to datetime objects, add two new columns
df$Date <- mdy(df$Date)
df$nextVWC_Observation <- 0.0
df$daysUntilNextObservation <- 0
df$CWB <- 0.0
df$NonZeroRain <- FALSE
df$CRain <- 0.0
df$CET <- 0.0
df$CIrr <- 0.0

#Iterate through all unique plots
for (i in unique(df$`Plot.No`)){
  sample <- df[df$`Plot.No` == i,]
  dates <- unique(sample$Date) #Get all unique dates for a given plot
  
  #Iterate through all unique dates minus 1
  for (j in 1:(length(unique(sample$Date))-1)){
    #Find next observation, find number of days, update observation columns.
    datediff <- as.integer(abs(difftime(dates[j], dates[j+1], units = "days")))
    thisIndex <- which(df$`Plot.No` == i & df$Date == dates[j])
    nextIndex <- which(df$`Plot.No` == i & df$Date == dates[j+1])
    df$nextVWC_Observation[thisIndex] <- df$`Mean.VWC`[nextIndex]
    df$daysUntilNextObservation[thisIndex] <- datediff
    
    thisWater <- df$CumNet[thisIndex]
    nextWater <- df$CumNet[nextIndex]
    diff <- nextWater - thisWater
    diffCopy <- nextWater - thisWater
    if(df$Irrigated.After[thisIndex] == "Yes"){
      diff <- diff + 0.25
      df$CIrr[thisIndex] <- 0.25
    }
    
    thisRain <- df$CumulativeRainfall[thisIndex]
    nextRain <- df$CumulativeRainfall[nextIndex]
    if (nextRain - thisRain > 0){
      df$NonZeroRain[thisIndex] <- TRUE
    }
    
    df$CRain[thisIndex] <- (nextRain - thisRain)
    df$CWB[thisIndex] <- diff
    df$CET[thisIndex] <- diffCopy - (nextRain - thisRain)
  }
}

write_csv(df, "C:/Users/Logan/Desktop/School Files/Senior Project/Shared_Dat/SIM_VERIFY.csv") #save

