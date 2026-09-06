# Baseline values predict end-of-year mathematics score: a correlational analysis

## Abstract

Background: A cohort study of a peer-tutoring program in secondary schools. Methods: The relationship between the baseline value and the log-transformed end-of-year mathematics score (0-100) was quantified with the Spearman rank correlation coefficient, first in the full analysis sample and then within the tutoring group only. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a cohort study of a peer-tutoring program in secondary schools. The primary question was whether enrolment in the peer-tutoring program is associated with end-of-year mathematics score (0-100). The dataset accompanying this report (data.csv) contains one row per student and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 212 students. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `program`.

**Exclusion criteria and preprocessing.** Only students aged 18 to 80 years inclusive were included in the analysis. Students with missing values for math_score were excluded (complete-case analysis). After the exclusions above, observations whose end-of-year mathematics score (0-100) lay more than three sample standard deviations from the overall mean were treated as outliers and removed. Because the distribution of end-of-year mathematics score (0-100) was right-skewed, it was natural-log transformed before modelling (values below 1 were set to 1 before transformation).

**Statistical analysis.** The relationship between the baseline value and the log-transformed end-of-year mathematics score (0-100) was quantified with the Spearman rank correlation coefficient, first in the full analysis sample and then within the tutoring group only. Two-sided p-values are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Across all [n_all] students, the baseline value correlated with the outcome (r = [r_all], p [p_all]). Within the tutoring group (n = [n_tutoring]) the correlation was r = [r_tutoring].

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_all`: Number of students in the full correlation analysis
- `r_all`: Spearman rank correlation coefficient in the full sample
- `p_all`: Two-sided p-value of the full-sample correlation
- `n_tutoring`: Number of students in the tutoring group correlation analysis
- `r_tutoring`: Spearman rank correlation coefficient within the tutoring group

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
