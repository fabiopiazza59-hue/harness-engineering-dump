# Fasting glucose across baseline tertiles

## Abstract

Background: A dietary intervention study on fasting glucose. Methods: Participants were divided into three groups (low, middle, high) by tertiles of the baseline value, using the first and second tertile cut-points of the analysis sample (values equal to a cut-point were assigned to the lower group). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a dietary intervention study on fasting glucose. The primary question was whether the Mediterranean diet intervention is associated with fasting glucose (mg/dL) at follow-up. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 258 participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `diet`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for glucose_fu were excluded (complete-case analysis). After the exclusions above, observations whose fasting glucose (mg/dL) at follow-up lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** Participants were divided into three groups (low, middle, high) by tertiles of the baseline value, using the first and second tertile cut-points of the analysis sample (values equal to a cut-point were assigned to the lower group). Mean fasting glucose (mg/dL) at follow-up was compared across the three groups with a one-way analysis of variance; eta squared was computed as the between-group sum of squares divided by the total sum of squares. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The low, middle and high tertile groups comprised 75, 76 and 73 participants, with mean fasting glucose (mg/dL) at follow-up of 97.11, 99.62 and 108.95 respectively (F = 18.84, p < 0.001, eta^2 = 0.146).

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
