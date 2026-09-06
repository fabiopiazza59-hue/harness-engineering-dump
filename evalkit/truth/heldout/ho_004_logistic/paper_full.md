# Predictors of the study event in a field experiment on nitrogen fertilisation in grassland plots

## Abstract

Background: A field experiment on nitrogen fertilisation in grassland plots. Methods: The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with nitrogen fertilisation (coded 1 for fertilised, 0 for unfertilised), age and body-mass index as predictors. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a field experiment on nitrogen fertilisation in grassland plots. The primary question was whether nitrogen fertilisation is associated with above-ground biomass (g/m^2). The dataset accompanying this report (data.csv) contains one row per plot and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 345 plots. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `treatment`.

**Exclusion criteria and preprocessing.** Only plots aged 18 to 80 years inclusive were included in the analysis. Plots with missing values for biomass, bmi were excluded (complete-case analysis).

**Statistical analysis.** The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with nitrogen fertilisation (coded 1 for fertilised, 0 for unfertilised), age and body-mass index as predictors. Odds ratios with Wald 95% confidence intervals are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Among 293 plots there were 153 events. Nitrogen fertilisation was associated with an adjusted odds ratio of 2.26 (95% CI 1.39 to 3.66, p < 0.001); the odds ratio per year of age was 1.02.

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
