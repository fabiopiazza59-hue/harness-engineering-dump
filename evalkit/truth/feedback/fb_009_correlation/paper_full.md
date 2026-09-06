# Baseline values predict end-of-year mathematics score: a correlational analysis

## Abstract

Background: A cohort study of a peer-tutoring program in secondary schools. Methods: The relationship between the baseline value and end-of-year mathematics score (0-100) was quantified with the Pearson product-moment correlation coefficient, first in the full analysis sample and then within the tutoring group only. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a cohort study of a peer-tutoring program in secondary schools. The primary question was whether enrolment in the peer-tutoring program is associated with end-of-year mathematics score (0-100). The dataset accompanying this report (data.csv) contains one row per student and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 384 students. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `program`.

**Exclusion criteria and preprocessing.** Only students aged 18 to 80 years inclusive were included in the analysis. Students with missing values for math_score were excluded (complete-case analysis). After the exclusions above, observations whose end-of-year mathematics score (0-100) lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** The relationship between the baseline value and end-of-year mathematics score (0-100) was quantified with the Pearson product-moment correlation coefficient, first in the full analysis sample and then within the tutoring group only. Two-sided p-values are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Across all 350 students, the baseline value correlated with the outcome (r = 0.446, p < 0.001). Within the tutoring group (n = 182) the correlation was r = 0.474.

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
