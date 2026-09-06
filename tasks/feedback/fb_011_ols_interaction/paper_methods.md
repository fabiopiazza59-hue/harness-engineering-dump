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

In the [n_model] records analysed, the exposure coefficient was [coef_exposure] (HC3 SE [se_exposure_hc3], p [p_exposure]); the interaction with centred age was [coef_interaction] (p [p_interaction]) and the BMI coefficient [coef_bmi] (R^2 = [r_squared]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_model`: Number of records in the model
- `coef_exposure`: Coefficient of the exposure (at mean age)
- `se_exposure_hc3`: HC3 robust standard error of the exposure coefficient
- `p_exposure`: p-value of the exposure coefficient (HC3)
- `coef_interaction`: Coefficient of the exposure x centred-age interaction
- `p_interaction`: p-value of the interaction term (HC3)
- `coef_bmi`: Coefficient of BMI
- `r_squared`: R squared

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
