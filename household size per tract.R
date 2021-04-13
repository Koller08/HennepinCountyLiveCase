setwd("D:/UMN/06_6130 Introduction to Business Analytics in R/Hennepin County Live Case")

library(tidyverse)
library(dplyr)
library(readxl)
library(tidyr)


# tract household size
tract <- read_excel("hennepin_county_all_tracts_household_size_us_census_2018 - Copy.xlsx",
                    skip=9)

tract <- tract[3, grepl("Tract", names(tract))]
tract <- gather(tract)
tract$key <- gsub(", Hennepin County, Minnesota", "", tract$key)
tract$key <- gsub("Census Tract ", "", tract$key)
tract$value <- gsub(",", "", tract$value)

tract$key <- as.numeric(tract$key)
tract$value <- as.numeric(tract$value)

tract <- tract %>%
  rename(tract_name = key,
         household_size = value)


# tract household margin
margin <- read_excel("hennepin_county_all_tracts_household_size_us_census_2018 - Copy.xlsx",
                    skip=9)
margin <- margin[3,]
margin <- gather(margin)
margin <- margin[grepl("±",margin$value), ]

margin$value <- gsub("±", "", margin$value)

margin$key <- as.numeric(margin$key)
margin$value <- as.numeric(margin$value)

margin <- margin %>%
  rename(error = value)

# combine the two
tract <- cbind(tract, margin$error)
tract <- tract %>%
  rename(error = `margin$error`)
