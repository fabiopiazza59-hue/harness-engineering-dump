# Adjusted association between participation in the financial coaching program and monthly savings

## Abstract

Background: An evaluation of a household financial coaching program. Methods: The association between participation in the financial coaching program and monthly savings (USD) was estimated with an ordinary least squares linear regression adjusted for age, body-mass index and the baseline value. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report an evaluation of a household financial coaching program. The primary question was whether participation in the financial coaching program is associated with monthly savings (USD). The dataset accompanying this report (data.csv) contains one row per household and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 384 households. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `program`.

**Exclusion criteria and preprocessing.** Only households aged 18 to 80 years inclusive were included in the analysis. Households with missing values for savings, bmi were excluded (complete-case analysis). After the exclusions above, observations whose monthly savings (USD) lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** The association between participation in the financial coaching program and monthly savings (USD) was estimated with an ordinary least squares linear regression adjusted for age, body-mass index and the baseline value. The exposure was coded 1 for coaching and 0 for none. Covariates were entered on their original scale. Conventional (non-robust) standard errors are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The adjusted model included [n_model] households. Participation in the financial coaching program was associated with a change of [coef_exposure] (SE [se_exposure], p [p_exposure]) in monthly savings (USD); the coefficient for age was [coef_age]. The model explained R^2 = [r_squared] (adjusted R^2 = [adj_r_squared]) of the variance.

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_model`: Number of households included in the regression model
- `coef_exposure`: Adjusted regression coefficient for participation in the financial coaching program
- `se_exposure`: Standard error of the exposure coefficient
- `p_exposure`: Two-sided p-value for the exposure coefficient
- `coef_age`: Adjusted regression coefficient for age (as entered in the model)
- `r_squared`: R squared of the model
- `adj_r_squared`: Adjusted R squared of the model

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
