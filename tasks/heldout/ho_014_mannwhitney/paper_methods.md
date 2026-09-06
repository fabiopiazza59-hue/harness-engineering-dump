# Distribution-free comparison of above-ground biomass by group

## Abstract

Background: A field experiment on nitrogen fertilisation in grassland plots. Methods: Above-ground biomass (g/m^2) was compared between the fertilised and unfertilised groups with a two-sided Mann-Whitney U test (asymptotic method with continuity correction). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a field experiment on nitrogen fertilisation in grassland plots. The primary question concerns nitrogen fertilisation and above-ground biomass (g/m^2). The accompanying dataset (data.csv) contains one row per plot-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 268 records. Variables are listed in the data dictionary. Group membership is recorded in `treatment`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only plots aged 18 to 80 years inclusive were analysed. Group labels in `treatment` were entered free-text and were normalised by trimming whitespace and lower-casing before use. Records with missing biomass were excluded (complete-case analysis).

**Statistical analysis.** Above-ground biomass (g/m^2) was compared between the fertilised and unfertilised groups with a two-sided Mann-Whitney U test (asymptotic method with continuity correction). The U statistic is reported for the fertilised group. The rank-biserial correlation was computed as 1 - 2U/(n1 n2). Medians and the difference in medians (fertilised minus unfertilised) are reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

The fertilised group (n = [n_fertilised], median [median_fertilised]) differed from the unfertilised group (n = [n_unfertilised], median [median_unfertilised]); the difference in medians was [median_diff] (U = [u_stat], p [p_value], rank-biserial r = [rank_biserial]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_unfertilised`: Number of plots in the unfertilised group
- `n_fertilised`: Number of plots in the fertilised group
- `median_unfertilised`: Median above-ground biomass (g/m^2) in the unfertilised group
- `median_fertilised`: Median above-ground biomass (g/m^2) in the fertilised group
- `median_diff`: Difference in medians (fertilised minus unfertilised)
- `u_stat`: Mann-Whitney U statistic for the fertilised group
- `p_value`: Two-sided p-value
- `rank_biserial`: Rank-biserial correlation 1 - 2U/(n1 n2)

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
