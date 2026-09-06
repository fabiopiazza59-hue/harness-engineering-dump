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

Among [n_pairs] participants the mean value changed from [mean_first] to [mean_second], a mean change of [mean_change] (SD [sd_change]; statistic = [t_stat], p [p_value]; dz = [cohens_dz]); the mean percent change was [mean_pct_change]%.

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_pairs`: Number of participants with both assessments in the analysis
- `mean_first`: Mean reaction time (ms) on the Stroop task at the first assessment
- `mean_second`: Mean at the second assessment
- `mean_change`: Mean change (second minus first)
- `sd_change`: Sample SD of the paired differences
- `t_stat`: Test statistic of the paired test
- `p_value`: Two-sided p-value of the paired test
- `cohens_dz`: Cohen's dz
- `mean_pct_change`: Mean per-subject percent change

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
