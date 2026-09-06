# Does age modify the effect of enrolment in the peer-tutoring program on end-of-year mathematics score?

## Abstract

Background: A cohort study of a peer-tutoring program in secondary schools. Methods: Body-mass index was derived as weight in kg divided by height in metres squared, and students with an implausible BMI (below 15 or above 50) were excluded. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a cohort study of a peer-tutoring program in secondary schools. The primary question concerns enrolment in the peer-tutoring program and end-of-year mathematics score (0-100). The accompanying dataset (data.csv) contains one row per student-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 451 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only students aged 18 to 80 years inclusive were analysed. Records with missing math_score, weight_kg, height_cm were excluded (complete-case analysis).

**Statistical analysis.** Body-mass index was derived as weight in kg divided by height in metres squared, and students with an implausible BMI (below 15 or above 50) were excluded. Age was centred at the mean of the analysis sample. End-of-year mathematics score (0-100) was regressed on enrolment in the peer-tutoring program (1 = tutoring, 0 = standard), centred age, their product (interaction), and BMI, using ordinary least squares with heteroskedasticity-robust (HC3) standard errors. R squared is the ordinary R squared. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

In the 385 records analysed, the exposure coefficient was 4.69 (HC3 SE 1.13, p < 0.001); the interaction with centred age was -0.15 (p = 0.081) and the BMI coefficient 0.81 (R^2 = 0.162).

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
