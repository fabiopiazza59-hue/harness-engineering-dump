# Event rates by group in a two-arm randomised trial of an antihypertensive regimen

## Abstract

Background: A two-arm randomised trial of an antihypertensive regimen. Methods: The proportion of patients with the study event was compared between the treatment and control groups with a Pearson chi-square test of independence without continuity correction. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a two-arm randomised trial of an antihypertensive regimen. The primary question was whether assignment to the treatment arm is associated with systolic blood pressure (mmHg) at 12 weeks. The dataset accompanying this report (data.csv) contains one row per patient and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 305 patients. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `arm`.

**Exclusion criteria and preprocessing.** Only patients aged 18 to 80 years inclusive were included in the analysis. Patients with missing values for sbp_12w were excluded (complete-case analysis).

**Statistical analysis.** The proportion of patients with the study event was compared between the treatment and control groups with a Pearson chi-square test of independence without continuity correction. The risk ratio is reported as the event proportion in the treatment group divided by that in the control group. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Of [n_treatment] patients in the treatment group, [events_treatment] experienced the event (proportion [prop_treatment]) compared with a proportion of [prop_control] among the [n_control] in the control group (risk ratio [risk_ratio]; chi-square = [chi2_stat], p [p_value]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_control`: Number of patients in the control group
- `n_treatment`: Number of patients in the treatment group
- `events_treatment`: Number of events in the treatment group
- `prop_control`: Proportion with the event in the control group
- `prop_treatment`: Proportion with the event in the treatment group
- `risk_ratio`: Risk ratio (treatment over control)
- `chi2_stat`: Pearson chi-square statistic (no continuity correction)
- `p_value`: p-value of the chi-square test

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
