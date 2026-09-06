# Predictors of the study event in an evaluation of a household financial coaching program

## Abstract

Background: An evaluation of a household financial coaching program. Methods: The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with participation in the financial coaching program (coded 1 for coaching, 0 for none), age and body-mass index as predictors. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report an evaluation of a household financial coaching program. The primary question was whether participation in the financial coaching program is associated with monthly savings (USD). The dataset accompanying this report (data.csv) contains one row per household and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 237 households. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `program`.

**Exclusion criteria and preprocessing.** Only households aged 18 to 80 years inclusive were included in the analysis. Households with missing values for savings, bmi were excluded (complete-case analysis).

**Statistical analysis.** The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with participation in the financial coaching program (coded 1 for coaching, 0 for none), age and body-mass index as predictors. Odds ratios with Wald 95% confidence intervals are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Among 207 households there were 115 events. Participation in the financial coaching program was associated with an adjusted odds ratio of 1.84 (95% CI 1.04 to 3.25, p = 0.036); the odds ratio per year of age was 1.01.

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
