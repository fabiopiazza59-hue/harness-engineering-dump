# Effect of nitrogen fertilisation on above-ground biomass: a field experiment on nitrogen fertilisation in grassland plots

## Abstract

Background: A field experiment on nitrogen fertilisation in grassland plots. Methods: The primary analysis compared the mean above-ground biomass (g/m^2) between the fertilised and unfertilised groups using an unpaired Student t-test assuming equal variances, two-sided. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a field experiment on nitrogen fertilisation in grassland plots. The primary question was whether nitrogen fertilisation is associated with above-ground biomass (g/m^2). The dataset accompanying this report (data.csv) contains one row per plot and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 382 plots. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `treatment`.

**Exclusion criteria and preprocessing.** Only plots aged 18 to 80 years inclusive were included in the analysis. Plots with missing values for biomass were excluded (complete-case analysis). After the exclusions above, observations whose above-ground biomass (g/m^2) lay more than three sample standard deviations from the overall mean were treated as outliers and removed.

**Statistical analysis.** The primary analysis compared the mean above-ground biomass (g/m^2) between the fertilised and unfertilised groups using an unpaired Student t-test assuming equal variances, two-sided. Group means and sample standard deviations (n - 1 denominator) are reported. The mean difference is reported as fertilised minus unfertilised. Cohen's d was computed as the mean difference divided by the pooled standard deviation. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

The primary analysis included [n_unfertilised] plots in the unfertilised group and [n_fertilised] in the fertilised group. Mean above-ground biomass (g/m^2) was [mean_unfertilised] in the unfertilised group and [mean_fertilised] (SD [sd_fertilised]) in the fertilised group, a difference of [mean_diff] (t = [t_stat], p [p_value]; Cohen's d = [cohens_d]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_unfertilised`: Number of plots in the unfertilised group included in the primary analysis
- `n_fertilised`: Number of plots in the fertilised group included in the primary analysis
- `mean_unfertilised`: Mean above-ground biomass (g/m^2) in the unfertilised group
- `mean_fertilised`: Mean above-ground biomass (g/m^2) in the fertilised group
- `sd_fertilised`: Sample standard deviation of above-ground biomass (g/m^2) in the fertilised group
- `mean_diff`: Mean difference in above-ground biomass (g/m^2) (fertilised minus unfertilised)
- `t_stat`: t statistic of the primary between-group test
- `p_value`: Two-sided p-value of the primary between-group test
- `cohens_d`: Cohen's d (pooled SD) for the between-group difference

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
