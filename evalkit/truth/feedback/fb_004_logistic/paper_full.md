# Predictors of the study event in a dietary intervention study on fasting glucose

## Abstract

Background: A dietary intervention study on fasting glucose. Methods: The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with the Mediterranean diet intervention (coded 1 for mediterranean, 0 for usual), age and body-mass index as predictors. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a dietary intervention study on fasting glucose. The primary question was whether the Mediterranean diet intervention is associated with fasting glucose (mg/dL) at follow-up. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 193 participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `diet`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for glucose_fu, bmi were excluded (complete-case analysis).

**Statistical analysis.** The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with the Mediterranean diet intervention (coded 1 for mediterranean, 0 for usual), age and body-mass index as predictors. Odds ratios with Wald 95% confidence intervals are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Among 161 participants there were 59 events. The mediterranean diet intervention was associated with an adjusted odds ratio of 0.35 (95% CI 0.16 to 0.73, p = 0.005); the odds ratio per year of age was 1.02.

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
