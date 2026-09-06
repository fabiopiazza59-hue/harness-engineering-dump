# Baseline values predict fasting glucose: a correlational analysis

## Abstract

Background: A dietary intervention study on fasting glucose. Methods: The relationship between the baseline value and fasting glucose (mg/dL) at follow-up was quantified with the Pearson product-moment correlation coefficient, first in the full analysis sample and then within the mediterranean group only. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a dietary intervention study on fasting glucose. The primary question was whether the Mediterranean diet intervention is associated with fasting glucose (mg/dL) at follow-up. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 245 participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `diet`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for glucose_fu were excluded (complete-case analysis). After the exclusions above, observations whose fasting glucose (mg/dL) at follow-up lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** The relationship between the baseline value and fasting glucose (mg/dL) at follow-up was quantified with the Pearson product-moment correlation coefficient, first in the full analysis sample and then within the mediterranean group only. Two-sided p-values are reported. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Across all [n_all] participants, the baseline value correlated with the outcome (r = [r_all], p [p_all]). Within the mediterranean group (n = [n_mediterranean]) the correlation was r = [r_mediterranean].

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_all`: Number of participants in the full correlation analysis
- `r_all`: Pearson product-moment correlation coefficient in the full sample
- `p_all`: Two-sided p-value of the full-sample correlation
- `n_mediterranean`: Number of participants in the mediterranean group correlation analysis
- `r_mediterranean`: Pearson product-moment correlation coefficient within the mediterranean group

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
