# Does age modify the effect of participation in the financial coaching program on monthly savings?

## Abstract

Background: An evaluation of a household financial coaching program. Methods: Body-mass index was derived as weight in kg divided by height in metres squared, and households with an implausible BMI (below 15 or above 50) were excluded. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report an evaluation of a household financial coaching program. The primary question concerns participation in the financial coaching program and monthly savings (USD). The accompanying dataset (data.csv) contains one row per household-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 305 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only households aged 18 to 80 years inclusive were analysed. Records with missing savings, weight_kg, height_cm were excluded (complete-case analysis).

**Statistical analysis.** Body-mass index was derived as weight in kg divided by height in metres squared, and households with an implausible BMI (below 15 or above 50) were excluded. Age was centred at the mean of the analysis sample. Monthly savings (usd) was regressed on participation in the financial coaching program (1 = coaching, 0 = waitlist), centred age, their product (interaction), and BMI, using ordinary least squares with heteroskedasticity-robust (HC3) standard errors. R squared is the ordinary R squared. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

In the 267 records analysed, the exposure coefficient was 58.93 (HC3 SE 12.18, p < 0.001); the interaction with centred age was 3.75 (p < 0.001) and the BMI coefficient -0.16 (R^2 = 0.190).

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
