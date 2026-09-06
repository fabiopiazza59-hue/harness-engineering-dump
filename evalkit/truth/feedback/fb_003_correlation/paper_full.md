# Baseline values predict reaction time: a correlational analysis

## Abstract

Background: A laboratory study of caffeine and attention. Methods: The relationship between the baseline value and the log-transformed reaction time (ms) on the Stroop task was quantified with the Spearman rank correlation coefficient, first in the full analysis sample and then within the caffeine group only. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a laboratory study of caffeine and attention. The primary question was whether caffeine administration is associated with reaction time (ms) on the Stroop task. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 263 participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `condition`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for rt_ms were excluded (complete-case analysis). After the exclusions above, observations whose reaction time (ms) on the Stroop task lay more than three sample standard deviations from the overall mean were treated as outliers and removed. Because the distribution of reaction time (ms) on the Stroop task was right-skewed, it was natural-log transformed before modelling (values below 1 were set to 1 before transformation).

**Statistical analysis.** The relationship between the baseline value and the log-transformed reaction time (ms) on the Stroop task was quantified with the Spearman rank correlation coefficient, first in the full analysis sample and then within the caffeine group only. Two-sided p-values are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Across all 219 participants, the baseline value correlated with the outcome (r = 0.574, p < 0.001). Within the caffeine group (n = 105) the correlation was r = 0.571.

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
