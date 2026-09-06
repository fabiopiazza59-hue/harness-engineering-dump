# Within-participant change in reaction time between two assessments

## Abstract

Background: A laboratory study of caffeine and attention. Methods: The change in reaction time (ms) on the Stroop task from the first to the second assessment was tested with a paired t-test (two-sided). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a laboratory study of caffeine and attention. The primary question concerns caffeine administration and reaction time (ms) on the Stroop task. The accompanying dataset (data.csv) contains one row per participant-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 246 records. Variables are listed in the data dictionary. Group membership is recorded in `condition`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only participants aged 18 to 80 years inclusive were analysed. Records with missing rt_ms, rt_ms_post were excluded (complete-case analysis).

**Statistical analysis.** The change in reaction time (ms) on the Stroop task from the first to the second assessment was tested with a paired t-test (two-sided). The mean change is the mean of (second minus first) over analysed participants; its standard deviation is the sample SD of the paired differences. Cohen's dz is the mean change divided by the SD of the differences. Percent change was computed per participant as (second - first) / first x 100 and then averaged. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among 211 participants the mean value changed from 696.07 to 672.71, a mean change of -23.36 (SD 44.46; statistic = -7.63, p < 0.001; dz = -0.525); the mean percent change was -3.38%.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
