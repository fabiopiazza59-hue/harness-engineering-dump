## Abstract

**Background:** A dietary intervention study on fasting glucose. **Methods:** The primary analysis compared the mean fasting glucose (mg/dL) at follow-up between the mediterranean and usual groups using an unpaired Student t-test assuming equal variances, two-sided. **Results:** see the Results section. **Conclusion:** the findings are discussed in the context of the analysis sample.

## Introduction

We report a dietary intervention study on fasting glucose. The primary question was whether the Mediterranean diet intervention is associated with fasting glucose (mg/dL) at follow-up. The dataset accompanying this report (data.csv) contains one row per participant and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for [n_total_collected] participants. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `diet`.

**Exclusion criteria and preprocessing.** Only participants aged 18 to 80 years inclusive were included in the analysis. Participants with missing values for `glucose_fu` were excluded (complete-case analysis). After the exclusions above, observations whose fasting glucose (mg/dL) at follow-up lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** The primary analysis compared the mean fasting glucose (mg/dL) at follow-up between the mediterranean and usual groups using an unpaired Student t-test assuming equal variances, two-sided. Group means and sample standard deviations (n - 1 denominator) are reported. The mean difference is reported as mediterranean minus usual. Cohen's d was computed as the mean difference divided by the pooled standard deviation. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The primary analysis included [n_usual] participants in the usual group and [n_mediterranean] participants in the mediterranean group. Mean fasting glucose (mg/dL) at follow-up was [mean_glucose_usual] in the usual group and [mean_glucose_mediterranean] (SD [sd_glucose_mediterranean]) in the mediterranean group, a difference of [mean_difference] (t = [t_statistic], p = [p_value]; Cohen's d = [cohens_d]).

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.