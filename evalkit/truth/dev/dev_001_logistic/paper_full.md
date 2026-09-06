# Predictors of the study event in a two-arm randomised trial of an antihypertensive regimen

## Abstract

Background: A two-arm randomised trial of an antihypertensive regimen. Methods: The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with assignment to the treatment arm (coded 1 for treatment, 0 for control), age and body-mass index as predictors. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a two-arm randomised trial of an antihypertensive regimen. The primary question was whether assignment to the treatment arm is associated with systolic blood pressure (mmHg) at 12 weeks. The dataset accompanying this report (data.csv) contains one row per patient and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 406 patients. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `arm`.

**Exclusion criteria and preprocessing.** Only patients aged 18 to 80 years inclusive were included in the analysis. Patients with missing values for sbp_12w, bmi were excluded (complete-case analysis).

**Statistical analysis.** The odds of the study event were modelled with a maximum-likelihood logistic regression (no penalisation) with assignment to the treatment arm (coded 1 for treatment, 0 for control), age and body-mass index as predictors. Odds ratios with Wald 95% confidence intervals are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Among 322 patients there were 112 events. Assignment to the treatment arm was associated with an adjusted odds ratio of 0.44 (95% CI 0.27 to 0.73, p = 0.001); the odds ratio per year of age was 1.03.

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
