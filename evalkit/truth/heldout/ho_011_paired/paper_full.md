# Within-patient change in systolic blood pressure between two assessments

## Abstract

Background: A two-arm randomised trial of an antihypertensive regimen. Methods: The change in systolic blood pressure (mmHg) at 12 weeks from the first to the second assessment was tested with a Wilcoxon signed-rank test (two-sided, normal approximation without continuity correction, zero differences discarded). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a two-arm randomised trial of an antihypertensive regimen. The primary question concerns assignment to the treatment arm and systolic blood pressure (mmHg) at 12 weeks. The accompanying dataset (data.csv) contains one row per patient-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 258 records. Variables are listed in the data dictionary. Group membership is recorded in `arm`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only patients aged 18 to 80 years inclusive were analysed. Records with missing sbp_12w, sbp_12w_post were excluded (complete-case analysis).

**Statistical analysis.** The change in systolic blood pressure (mmHg) at 12 weeks from the first to the second assessment was tested with a Wilcoxon signed-rank test (two-sided, normal approximation without continuity correction, zero differences discarded). The mean change is the mean of (second minus first) over analysed patients; its standard deviation is the sample SD of the paired differences. Cohen's dz is the mean change divided by the SD of the differences. Percent change was computed per patient as (second - first) / first x 100 and then averaged. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among 220 patients the mean value changed from 135.85 to 130.93, a mean change of -4.92 (SD 5.73; statistic = 2586.50, p < 0.001; dz = -0.859); the mean percent change was -3.65%.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
