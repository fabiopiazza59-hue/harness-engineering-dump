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

The adjusted model included 212 participants. Caffeine administration was associated with a change of -56.37 (SE 13.61, p < 0.001) in reaction time (ms) on the Stroop task; the coefficient for age was -3.62. The model explained R^2 = 0.357 (adjusted R^2 = 0.345) of the variance.

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
