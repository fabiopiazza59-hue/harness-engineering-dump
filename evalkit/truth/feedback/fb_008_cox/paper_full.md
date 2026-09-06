# Time to the study event by nitrogen fertilisation: a survival analysis

## Abstract

Background: A field experiment on nitrogen fertilisation in grassland plots. Methods: Follow-up time in days was computed from the enrolment date to the date of event or last contact. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a field experiment on nitrogen fertilisation in grassland plots. The primary question concerns nitrogen fertilisation and above-ground biomass (g/m^2). The accompanying dataset (data.csv) contains one row per plot-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 419 records. Variables are listed in the data dictionary. Group membership is recorded in `treatment`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only plots aged 18 to 80 years inclusive were analysed. Group labels in `treatment` were entered free-text and were normalised by trimming whitespace and lower-casing before use.

**Statistical analysis.** Follow-up time in days was computed from the enrolment date to the date of event or last contact. Follow-up was administratively censored at 730 days: plots with longer follow-up were censored at 730 days and counted as event-free, and records with zero follow-up were excluded. The hazard of the study event was modelled with a Cox proportional-hazards model with nitrogen fertilisation (1 = fertilised, 0 = unfertilised) and age (years) as covariates, using the Breslow method for ties. Hazard ratios with Wald 95% confidence intervals (z = 1.96) are reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Of 404 plots (median follow-up 285.00 days), 250 had an event. The exposure hazard ratio was 1.48 (95% CI 1.15 to 1.89, p = 0.002); the hazard ratio per year of age was 1.01.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
