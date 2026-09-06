# Biomarker correlates of reaction time with false-discovery-rate control

## Abstract

Background: A laboratory study of caffeine and attention. Methods: Each of the six biomarkers was correlated with reaction time (ms) on the Stroop task using Pearson correlation (two-sided). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a laboratory study of caffeine and attention. The primary question concerns caffeine administration and reaction time (ms) on the Stroop task. The accompanying dataset (data.csv) contains one row per participant-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 390 records. Variables are listed in the data dictionary. Group membership is recorded in `condition`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only participants aged 18 to 80 years inclusive were analysed. Records with missing rt_ms, biomarker_1, biomarker_2, biomarker_3, biomarker_4, biomarker_5, biomarker_6 were excluded (complete-case analysis).

**Statistical analysis.** Each of the six biomarkers was correlated with reaction time (ms) on the Stroop task using Pearson correlation (two-sided). The six p-values were adjusted for multiple testing with the Benjamini-Hochberg false-discovery-rate procedure; associations with adjusted p < 0.05 were declared significant. The strongest association is the biomarker with the largest absolute correlation. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among [n_analysed] participants, biomarker_1 correlated with the outcome (r = [r_biomarker_1], adjusted p [p_adj_biomarker_1]), as did biomarker_3 (r = [r_biomarker_3], adjusted p [p_adj_biomarker_3]); the adjusted p for biomarker_5 was [p_adj_biomarker_5]. In total [n_significant_adj] biomarkers remained significant after adjustment; the strongest association had r = [r_strongest].

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_analysed`: Number of participants with all biomarkers and the outcome
- `r_biomarker_1`: Pearson r of biomarker_1 with the outcome
- `p_adj_biomarker_1`: BH-adjusted p-value for biomarker_1
- `r_biomarker_3`: Pearson r of biomarker_3 with the outcome
- `p_adj_biomarker_3`: BH-adjusted p-value for biomarker_3
- `p_adj_biomarker_5`: BH-adjusted p-value for biomarker_5
- `n_significant_adj`: Number of biomarkers significant after BH adjustment (adjusted p < 0.05)
- `r_strongest`: Signed Pearson r of the biomarker with the largest absolute correlation

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
