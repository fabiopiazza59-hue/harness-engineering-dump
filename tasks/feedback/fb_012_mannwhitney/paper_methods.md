# Distribution-free comparison of monthly savings by group

## Abstract

Background: An evaluation of a household financial coaching program. Methods: Monthly savings (usd) was compared between the coaching and waitlist groups with a two-sided Mann-Whitney U test (asymptotic method with continuity correction). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report an evaluation of a household financial coaching program. The primary question concerns participation in the financial coaching program and monthly savings (USD). The accompanying dataset (data.csv) contains one row per household-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 453 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only households aged 18 to 80 years inclusive were analysed. Group labels in `program` were entered free-text and were normalised by trimming whitespace and lower-casing before use. Records with missing savings were excluded (complete-case analysis).

**Statistical analysis.** Monthly savings (usd) was compared between the coaching and waitlist groups with a two-sided Mann-Whitney U test (asymptotic method with continuity correction). The U statistic is reported for the coaching group. The rank-biserial correlation was computed as 1 - 2U/(n1 n2). Medians and the difference in medians (coaching minus waitlist) are reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

The coaching group (n = [n_coaching], median [median_coaching]) differed from the waitlist group (n = [n_waitlist], median [median_waitlist]); the difference in medians was [median_diff] (U = [u_stat], p [p_value], rank-biserial r = [rank_biserial]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_waitlist`: Number of households in the waitlist group
- `n_coaching`: Number of households in the coaching group
- `median_waitlist`: Median monthly savings (USD) in the waitlist group
- `median_coaching`: Median monthly savings (USD) in the coaching group
- `median_diff`: Difference in medians (coaching minus waitlist)
- `u_stat`: Mann-Whitney U statistic for the coaching group
- `p_value`: Two-sided p-value
- `rank_biserial`: Rank-biserial correlation 1 - 2U/(n1 n2)

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
