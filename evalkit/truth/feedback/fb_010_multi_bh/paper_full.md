# Biomarker correlates of monthly savings with false-discovery-rate control

## Abstract

Background: An evaluation of a household financial coaching program. Methods: Each of the six biomarkers was correlated with monthly savings (USD) using Pearson correlation (two-sided). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report an evaluation of a household financial coaching program. The primary question concerns participation in the financial coaching program and monthly savings (USD). The accompanying dataset (data.csv) contains one row per household-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 333 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only households aged 18 to 80 years inclusive were analysed. Records with missing savings, biomarker_1, biomarker_2, biomarker_3, biomarker_4, biomarker_5, biomarker_6 were excluded (complete-case analysis).

**Statistical analysis.** Each of the six biomarkers was correlated with monthly savings (USD) using Pearson correlation (two-sided). The six p-values were adjusted for multiple testing with the Benjamini-Hochberg false-discovery-rate procedure; associations with adjusted p < 0.05 were declared significant. The strongest association is the biomarker with the largest absolute correlation. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among 291 households, biomarker_1 correlated with the outcome (r = 0.498, adjusted p < 0.001), as did biomarker_3 (r = -0.318, adjusted p < 0.001); the adjusted p for biomarker_5 was < 0.001. In total 3 biomarkers remained significant after adjustment; the strongest association had r = 0.498.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
