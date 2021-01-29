library(tidyr)
library(tibble)
library(dplyr)

# begin where we left off
time_differences <- read.csv("Datasets/9t/time_differences.csv")

# HDI

hdi <- read.csv("Datasets/controls/human-development-index.csv")

# Standardize names
hdi<-rename(hdi, score = Human.Development.Index..UNDP.)
hdi<-rename(hdi, country = Entity)
# Melt data
hdi_melt <- spread(hdi, Year, score)
hdi_melt <- select(hdi_melt, !Code)
# Get means for recent years
hdi_melt$hdi_m <- rowMeans(subset(hdi_melt,select = 2:31),na.rm=TRUE)
# Extract only the cols I care about
hdi_means <- select(hdi_melt,1,32)

# Age of democracy
age <- read.csv("Datasets/controls/age-of-democracies.csv")
# Standarize names
age <- rename(age,span_y=Age.of.democracies.at.the.end.of.2015..Boix..Miller..and.Rosato..2013..2018.)
# Fix messy column into number values
for (i in 1:nrow(age)){
  if (age$span_y[i] == "Not a democracy in 2015"){
    age$span_y[i] = "0"
  }
}
age_fixed<-rename(age_fixed,country=Entity)
age_fixed$span_y <- as.numeric(age_fixed$span_y)

# Religion. 
#This was ok. Only needed to standarize names
religion <- read.csv("Datasets/controls/main-religion-of-the-country-in.csv")
religion_fixed<-rename(religion,country=Entity)

# GDP
gdp <- read.csv("Datasets/controls/average-real-gdp-per-capita-across-countries-and-regions.csv")

# Standardize names
gdp <- rename(gdp,country = Entity)
gdp <- rename(gdp,gdp_v = Real.GDP.per.capita.in.2011US...multiple.benchmarks..Maddison.Project.Database..2018.. )
# Melt
gdp_melt <- spread(gdp, Year, gdp_v)
# Select only recent years
gdp_melt2 <- select(gdp_melt,country,718:743)
# Get row means
gdp_melt2$gdp_m <- rowMeans(subset(gdp_melt2,select = 2:27),na.rm=TRUE)
# Drop cols we don't care about
gdp_means <- select(gdp_melt2,1,28)

# Joins. Inner join drops a lot cases because of non-matching names. 
# this needs to be fixed
df_simple <- inner_join(time_differences,hdi_means,"country")
df_simple <- inner_join(df_simple,gdp_means,"country")
df_simple <- inner_join(df_simple,age_fixed,"country")
df_simple <- inner_join(df_simple,religion_fixed,"country")
# Drop repeated /useless variables
df_simple <- select(df_simple,!X)
df_simple <- select(df_simple,!Code.x)
df_simple <- select(df_simple,!Code.y)

glimpse(df_simple)
