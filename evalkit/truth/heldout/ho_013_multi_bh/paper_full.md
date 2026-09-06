# Biomarker correlates of systolic blood pressure with false-discovery-rate control

## Abstract

Background: A two-arm randomised trial of an antihypertensive regimen. Methods: Each of the six biomarkers was correlated with systolic blood pressure (mmHg) at 12 weeks using Pearson correlation (two-sided). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a two-arm randomised trial of an antihypertensive regimen. The primary question concerns assignment to the treatment arm and systolic blood pressure (mmHg) at 12 weeks. The accompanying dataset (data.csv) contains one row per patient-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 313 records. Variables are listed in the data dictionary. Group membership is recorded in `arm`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only patients aged 18 to 80 years inclusive were analysed. Records with missing sbp_12w, biomarker_1, biomarker_2, biomarker_3, biomarker_4, biomarker_5, biomarker_6 were excluded (complete-case analysis).

**Statistical analysis.** Each of the six biomarkers was correlated with systolic blood pressure (mmHg) at 12 weeks using Pearson correlation (two-sided). The six p-values were adjusted for multiple testing with the Benjamini-Hochberg false-discovery-rate procedure; associations with adjusted p < 0.05 were declared significant. The strongest association is the biomarker with the largest absolute correlation. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among 271 patients, biomarker_1 correlated with the outcome (r = 0.487, adjusted p < 0.001), as did biomarker_3 (r = -0.287, adjusted p < 0.001); the adjusted p for biomarker_5 was = 0.004. In total 4 biomarkers remained significant after adjustment; the strongest association had r = 0.487.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
