# Event rates by group in a two-arm randomised trial of an antihypertensive regimen

## Abstract

Background: A two-arm randomised trial of an antihypertensive regimen. Methods: The proportion of patients with the study event was compared between the treatment and control groups with a Pearson chi-square test of independence without continuity correction. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a two-arm randomised trial of an antihypertensive regimen. The primary question was whether assignment to the treatment arm is associated with systolic blood pressure (mmHg) at 12 weeks. The dataset accompanying this report (data.csv) contains one row per patient and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 338 patients. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `arm`.

**Exclusion criteria and preprocessing.** Only patients aged 18 to 80 years inclusive were included in the analysis. Patients with missing values for sbp_12w were excluded (complete-case analysis).

**Statistical analysis.** The proportion of patients with the study event was compared between the treatment and control groups with a Pearson chi-square test of independence without continuity correction. The risk ratio is reported as the event proportion in the treatment group divided by that in the control group. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Of 130 patients in the treatment group, 38 experienced the event (proportion 0.292) compared with a proportion of 0.476 among the 168 in the control group (risk ratio 0.61; chi-square = 10.36, p = 0.001).

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
