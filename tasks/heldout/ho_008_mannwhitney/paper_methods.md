# Distribution-free comparison of fasting glucose by group

## Abstract

Background: A dietary intervention study on fasting glucose. Methods: Fasting glucose (mg/dl) at follow-up was compared between the mediterranean and usual groups with a two-sided Mann-Whitney U test (asymptotic method with continuity correction). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a dietary intervention study on fasting glucose. The primary question concerns the Mediterranean diet intervention and fasting glucose (mg/dL) at follow-up. The accompanying dataset (data.csv) contains one row per participant-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 437 records. Variables are listed in the data dictionary. Group membership is recorded in `diet`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only participants aged 18 to 80 years inclusive were analysed. Group labels in `diet` were entered free-text and were normalised by trimming whitespace and lower-casing before use. Records with missing glucose_fu were excluded (complete-case analysis).

**Statistical analysis.** Fasting glucose (mg/dl) at follow-up was compared between the mediterranean and usual groups with a two-sided Mann-Whitney U test (asymptotic method with continuity correction). The U statistic is reported for the mediterranean group. The rank-biserial correlation was computed as 1 - 2U/(n1 n2). Medians and the difference in medians (mediterranean minus usual) are reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

The mediterranean group (n = [n_mediterranean], median [median_mediterranean]) differed from the usual group (n = [n_usual], median [median_usual]); the difference in medians was [median_diff] (U = [u_stat], p [p_value], rank-biserial r = [rank_biserial]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_usual`: Number of participants in the usual group
- `n_mediterranean`: Number of participants in the mediterranean group
- `median_usual`: Median fasting glucose (mg/dL) at follow-up in the usual group
- `median_mediterranean`: Median fasting glucose (mg/dL) at follow-up in the mediterranean group
- `median_diff`: Difference in medians (mediterranean minus usual)
- `u_stat`: Mann-Whitney U statistic for the mediterranean group
- `p_value`: Two-sided p-value
- `rank_biserial`: Rank-biserial correlation 1 - 2U/(n1 n2)

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
