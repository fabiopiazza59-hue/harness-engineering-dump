# Does age modify the effect of assignment to the treatment arm on systolic blood pressure?

## Abstract

Background: A two-arm randomised trial of an antihypertensive regimen. Methods: Body-mass index was derived as weight in kg divided by height in metres squared, and patients with an implausible BMI (below 15 or above 50) were excluded. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a two-arm randomised trial of an antihypertensive regimen. The primary question concerns assignment to the treatment arm and systolic blood pressure (mmHg) at 12 weeks. The accompanying dataset (data.csv) contains one row per patient-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 450 records. Variables are listed in the data dictionary. Group membership is recorded in `arm`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only patients aged 18 to 80 years inclusive were analysed. Records with missing sbp_12w, weight_kg, height_cm were excluded (complete-case analysis).

**Statistical analysis.** Body-mass index was derived as weight in kg divided by height in metres squared, and patients with an implausible BMI (below 15 or above 50) were excluded. Age was centred at the mean of the analysis sample. Systolic blood pressure (mmhg) at 12 weeks was regressed on assignment to the treatment arm (1 = treatment, 0 = control), centred age, their product (interaction), and BMI, using ordinary least squares with heteroskedasticity-robust (HC3) standard errors. R squared is the ordinary R squared. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

In the 401 records analysed, the exposure coefficient was -7.38 (HC3 SE 1.21, p < 0.001); the interaction with centred age was -0.12 (p = 0.223) and the BMI coefficient 0.51 (R^2 = 0.125).

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
