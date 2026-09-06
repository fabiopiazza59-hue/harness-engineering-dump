# Adjusted association between caffeine administration and reaction time

## Abstract

Background: A laboratory study of caffeine and attention. Methods: The association between caffeine administration and reaction time (ms) on the Stroop task was estimated with an ordinary least squares linear regression adjusted for age, body-mass index and the baseline value. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a laboratory study of caffeine and attention. The primary question was whether caffeine administration is associated with reaction time (ms) on the Stroop task. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 232 participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `condition`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for rt_ms, bmi were excluded (complete-case analysis).

**Statistical analysis.** The association between caffeine administration and reaction time (ms) on the Stroop task was estimated with an ordinary least squares linear regression adjusted for age, body-mass index and the baseline value. The exposure was coded 1 for caffeine and 0 for placebo. Covariates were entered on their original scale. Conventional (non-robust) standard errors are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The adjusted model included [n_model] participants. Caffeine administration was associated with a change of [coef_exposure] (SE [se_exposure], p [p_exposure]) in reaction time (ms) on the Stroop task; the coefficient for age was [coef_age]. The model explained R^2 = [r_squared] (adjusted R^2 = [adj_r_squared]) of the variance.

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_model`: Number of participants included in the regression model
- `coef_exposure`: Adjusted regression coefficient for caffeine administration
- `se_exposure`: Standard error of the exposure coefficient
- `p_exposure`: Two-sided p-value for the exposure coefficient
- `coef_age`: Adjusted regression coefficient for age (as entered in the model)
- `r_squared`: R squared of the model
- `adj_r_squared`: Adjusted R squared of the model

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
