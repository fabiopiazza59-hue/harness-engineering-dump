# Event rates by group in a field experiment on nitrogen fertilisation in grassland plots

## Abstract

Background: A field experiment on nitrogen fertilisation in grassland plots. Methods: The proportion of plots with the study event was compared between the fertilised and unfertilised groups with a Pearson chi-square test of independence without continuity correction. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a field experiment on nitrogen fertilisation in grassland plots. The primary question was whether nitrogen fertilisation is associated with above-ground biomass (g/m^2). The dataset accompanying this report (data.csv) contains one row per plot and is described in the data dictionary.

## Methods

**Participants and data.** Data were collected for 310 plots. Each record contains the variables listed in the data dictionary. Group membership is recorded in the column `treatment`.

**Exclusion criteria and preprocessing.** Only plots aged 18 to 80 years inclusive were included in the analysis. Plots with missing values for biomass were excluded (complete-case analysis).

**Statistical analysis.** The proportion of plots with the study event was compared between the fertilised and unfertilised groups with a Pearson chi-square test of independence without continuity correction. The risk ratio is reported as the event proportion in the fertilised group divided by that in the unfertilised group. All analyses were performed on the analysis sample defined above. Statistics were computed with standard scientific software; no random resampling was used.

## Results

Of [n_fertilised] plots in the fertilised group, [events_fertilised] experienced the event (proportion [prop_fertilised]) compared with a proportion of [prop_unfertilised] among the [n_unfertilised] in the unfertilised group (risk ratio [risk_ratio]; chi-square = [chi2_stat], p [p_value]).

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_unfertilised`: Number of plots in the unfertilised group
- `n_fertilised`: Number of plots in the fertilised group
- `events_fertilised`: Number of events in the fertilised group
- `prop_unfertilised`: Proportion with the event in the unfertilised group
- `prop_fertilised`: Proportion with the event in the fertilised group
- `risk_ratio`: Risk ratio (fertilised over unfertilised)
- `chi2_stat`: Pearson chi-square statistic (no continuity correction)
- `p_value`: p-value of the chi-square test

## Discussion

The analysis followed the pre-specified plan described in the Methods. Limitations include the observational nature of some comparisons and the exclusion of records with missing values.
