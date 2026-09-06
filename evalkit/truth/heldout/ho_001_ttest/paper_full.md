# Effect of caffeine administration on reaction time: a laboratory study

## Abstract

Background: A laboratory study of caffeine and attention. Methods: The primary analysis compared the mean reaction time (ms) on the Stroop task between the caffeine and placebo groups using an unpaired Welch t-test (unequal variances), two-sided. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a laboratory study of caffeine and attention. The primary question was whether caffeine administration is associated with reaction time (ms) on the Stroop task. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 204 participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `condition`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for rt_ms were excluded (complete-case analysis). After the exclusions above, observations whose reaction time (ms) on the Stroop task lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** The primary analysis compared the mean reaction time (ms) on the Stroop task between the caffeine and placebo groups using an unpaired Welch t-test (unequal variances), two-sided. Group means and sample standard deviations (n - 1 denominator) are reported. The mean difference is reported as caffeine minus placebo. Cohen's d was computed as the mean difference divided by the pooled standard deviation. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The primary analysis included 89 participants in the placebo group and 90 in the caffeine group. Mean reaction time (ms) on the Stroop task was 706.99 in the placebo group and 682.99 (SD 99.26) in the caffeine group, a difference of -24.00 (t = -1.60, p = 0.111; Cohen's d = -0.239).

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
