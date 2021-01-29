# Minimal imports. Tibble for glimpse.
library(readxl)
library(tibble)

# How to read a list of files. First get them into a variable. Will not work if the folder is not completely empty of extraneous files.

filenames <- list.files("C:/Users/gusta/Documents/Datasets/9t/", full.names=TRUE)

# Initialize empty list

df_list = list()

# Loop through the read excel function, with parameters

for (i in 1:length(filenames)){
  df_list[[i]] = read_excel(filenames[[i]],col_names=TRUE,col_types="guess",skip=1)  
}

# Create a list of names, pass it the list items with the names function to name them.

names(df_list) <-c('CAT','CEDAW','CPED','CRC','CRPD','ICCPR','ICERD','ICESCR','ICRMW')

# List to env. for getting them as variables

list2env(df_list,.GlobalEnv)

# Add opening date.
# use posixct to avoid incompatiblity with the way the df types were guessed

ICCPR['sdate'] = as.POSIXct("1966-12-06")
ICESCR['sdate'] = as.POSIXct("1966-12-06")
ICERD['sdate'] =  as.POSIXct("1965-12-21")
CEDAW['sdate'] =  as.POSIXct("1980-03-01")
CRC['sdate'] =  as.POSIXct("1989-11-20")
CAT['sdate'] =  as.POSIXct("1984-12-10")
CRPD['sdate'] =  as.POSIXct("1990-12-18")
ICRMW['sdate'] =  as.POSIXct("2007-02-06")
CPED['sdate'] =  as.POSIXct("2007-03-30")

# Get time differences. 

td_ICCPR <- as.numeric(ICCPR$`Date of Ratification/Accession`-ICCPR$sdate)
td_ICESCR <- as.numeric(ICESCR$`Date of Ratification/Accession`-ICESCR$sdate)
td_ICERD <- as.numeric(ICERD$`Date of Ratification/Accession`-ICERD$sdate)
td_CEDAW <- as.numeric(CEDAW$`Date of Ratification/Accession`-CEDAW$sdate)
td_CRC <- as.numeric(CRC$`Date of Ratification/Accession`-CRC$sdate)
td_CAT <- as.numeric(CAT$`Date of Ratification/Accession`-CAT$sdate)
td_CRPD <- as.numeric(CRPD$`Date of Ratification/Accession`-CRPD$sdate)
td_ICRMW <- as.numeric(ICRMW$`Date of Ratification/Accession`-ICRMW$sdate)
td_CPED <- as.numeric(CPED$`Date of Ratification/Accession`-CPED$sdate)

# Get a list of countries as the index

countries <- ICCPR$Country

# Build a dataframe from the series.

time_differences <- data.frame("country" = countries,
                               "td_ICCPR" = td_ICCPR, 
                               "td_ICESCR" = td_ICESCR, 
                               "td_ICERD" = td_ICERD,
                               "td_CEDAW" = td_CEDAW,
                               "td_CRC" = td_CRC,
                               "td_CAT" = td_CAT,
                               "td_CRPD" = td_CRPD,
                               "td_CPED" = td_CPED,
                               "td_ICRMW" = td_ICRMW)

glimpse(time_differences)

# Tests
# X<- ifelse(time_differences$td_ICCPR > 0,1,0)
# X<- ifelse(is.na(time_differences$td_ICCPR),0,1)

# Get the binaries

time_differences['bin_ICCPR'] <- ifelse(is.na(time_differences$td_ICCPR),0,1)
time_differences['bin_ICESCR'] <- ifelse(is.na(time_differences$td_ICESCR),0,1)
time_differences['bin_ICERD'] <- ifelse(is.na(time_differences$td_ICERD),0,1)
time_differences['bin_CEDAW'] <- ifelse(is.na(time_differences$td_CEDAW),0,1)
time_differences['bin_CRC'] <- ifelse(is.na(time_differences$td_CRC),0,1)
time_differences['bin_CAT'] <- ifelse(is.na(time_differences$td_CAT),0,1)
time_differences['bin_CRPD'] <- ifelse(is.na(time_differences$td_CRPD),0,1)
time_differences['bin_CPED'] <- ifelse(is.na(time_differences$td_CPED),0,1)
time_differences['bin_ICRMW'] <- ifelse(is.na(time_differences$td_ICRMW),0,1)

# At this point the dataset is ready

glimpse(time_differences)

# Some plottign for fun

X <- time_differences[3:11]
par(mfrow=c(3,3))
apply(X, 2, hist, col=heat.colors(9))

# write read the file

write.csv(time_differences, "C:/Users/gusta/Documents/Datasets/9t/time_differences.csv")
time_differences<-read.csv("C:/Users/gusta/Documents/Datasets/9t/time_differences.csv")

