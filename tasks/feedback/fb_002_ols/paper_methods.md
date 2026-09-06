# Adjusted association between nitrogen fertilisation and above-ground biomass

## Abstract

Background: A field experiment on nitrogen fertilisation in grassland plots. Methods: The association between nitrogen fertilisation and above-ground biomass (g/m^2) was estimated with an ordinary least squares linear regression adjusted for age, body-mass index and the baseline value. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a field experiment on nitrogen fertilisation in grassland plots. The primary question was whether nitrogen fertilisation is associated with above-ground biomass (g/m^2). The dataset accompanying this report (data.csv) contains one row per plot and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 243 plots. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `treatment`.

**Exclusion criteria and preprocessing.** Only plots aged 18 to 80 years inclusive were included in the analysis. Plots with missing values for biomass, bmi were excluded (complete-case analysis).

**Statistical analysis.** The association between nitrogen fertilisation and above-ground biomass (g/m^2) was estimated with an ordinary least squares linear regression adjusted for age, body-mass index and the baseline value. The exposure was coded 1 for fertilised and 0 for unfertilised. Covariates were entered on their original scale. Conventional (non-robust) standard errors are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The adjusted model included [n_model] plots. Nitrogen fertilisation was associated with a change of [coef_exposure] (SE [se_exposure], p [p_exposure]) in above-ground biomass (g/m^2); the coefficient for age was [coef_age]. The model explained R^2 = [r_squared] (adjusted R^2 = [adj_r_squared]) of the variance.

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_model`: Number of plots included in the regression model
- `coef_exposure`: Adjusted regression coefficient for nitrogen fertilisation
- `se_exposure`: Standard error of the exposure coefficient
- `p_exposure`: Two-sided p-value for the exposure coefficient
- `coef_age`: Adjusted regression coefficient for age (as entered in the model)
- `r_squared`: R squared of the model
- `adj_r_squared`: Adjusted R squared of the model

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
