# Reaction time across baseline tertiles

## Abstract

Background: A laboratory study of caffeine and attention. Methods: Participants were divided into three groups (low, middle, high) by tertiles of the baseline value, using the first and second tertile cut-points of the analysis sample (values equal to a cut-point were assigned to the lower group). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a laboratory study of caffeine and attention. The primary question was whether caffeine administration is associated with reaction time (ms) on the Stroop task. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 213 participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `condition`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for rt_ms were excluded (complete-case analysis). After the exclusions above, observations whose reaction time (ms) on the Stroop task lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** Participants were divided into three groups (low, middle, high) by tertiles of the baseline value, using the first and second tertile cut-points of the analysis sample (values equal to a cut-point were assigned to the lower group). Mean reaction time (ms) on the Stroop task was compared across the three groups with a one-way analysis of variance; eta squared was computed as the between-group sum of squares divided by the total sum of squares. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The low, middle and high tertile groups comprised [n_low], [n_middle] and [n_high] participants, with mean reaction time (ms) on the Stroop task of [mean_low], [mean_middle] and [mean_high] respectively (F = [f_stat], p [p_value], eta^2 = [eta_squared]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_low`: Number of participants in the low baseline tertile group
- `mean_low`: Mean reaction time (ms) on the Stroop task in the low tertile group
- `n_middle`: Number of participants in the middle baseline tertile group
- `mean_middle`: Mean reaction time (ms) on the Stroop task in the middle tertile group
- `n_high`: Number of participants in the high baseline tertile group
- `mean_high`: Mean reaction time (ms) on the Stroop task in the high tertile group
- `f_stat`: F statistic of the one-way ANOVA
- `p_value`: p-value of the one-way ANOVA
- `eta_squared`: Eta squared of the group factor

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
