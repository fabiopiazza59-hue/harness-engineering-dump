# Site-stratified association between the Mediterranean diet intervention and the study event

## Abstract

Background: A dietary intervention study on fasting glucose. Methods: The association between the Mediterranean diet intervention (exposed = mediterranean) and the study event was summarised with the crude odds ratio and with the Mantel-Haenszel odds ratio pooled across the four study sites (2x2 tables ordered exposed/unexposed by event/no event), with its 95% confidence interval, and the Mantel-Haenszel chi-square test with continuity correction. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a dietary intervention study on fasting glucose. The primary question concerns the Mediterranean diet intervention and fasting glucose (mg/dL) at follow-up. The accompanying dataset (data.csv) contains one row per participant-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 326 records. Variables are listed in the data dictionary. Group membership is recorded in `diet`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only participants aged 18 to 80 years inclusive were analysed. Group labels in `diet` were entered free-text and were normalised by trimming whitespace and lower-casing before use.

**Statistical analysis.** The association between the Mediterranean diet intervention (exposed = mediterranean) and the study event was summarised with the crude odds ratio and with the Mantel-Haenszel odds ratio pooled across the four study sites (2x2 tables ordered exposed/unexposed by event/no event), with its 95% confidence interval, and the Mantel-Haenszel chi-square test with continuity correction. The site-specific odds ratio for site 1 is also reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among 307 participants (164 exposed) the crude odds ratio was 0.57 and the Mantel-Haenszel odds ratio pooled over sites was 0.56 (95% CI 0.34 to 0.90; MH chi-square = 5.14, p = 0.023). Within site 1 the odds ratio was 1.02.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
