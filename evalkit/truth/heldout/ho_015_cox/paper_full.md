# Time to the study event by participation in the financial coaching program: a survival analysis

## Abstract

Background: An evaluation of a household financial coaching program. Methods: Follow-up time in days was computed from the enrolment date to the date of event or last contact. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report an evaluation of a household financial coaching program. The primary question concerns participation in the financial coaching program and monthly savings (USD). The accompanying dataset (data.csv) contains one row per household-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 303 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only households aged 18 to 80 years inclusive were analysed. Group labels in `program` were entered free-text and were normalised by trimming whitespace and lower-casing before use.

**Statistical analysis.** Follow-up time in days was computed from the enrolment date to the date of event or last contact. Follow-up was administratively censored at 730 days: households with longer follow-up were censored at 730 days and counted as event-free, and records with zero follow-up were excluded. The hazard of the study event was modelled with a Cox proportional-hazards model with participation in the financial coaching program (1 = coaching, 0 = waitlist) and age (years) as covariates, using the Breslow method for ties. Hazard ratios with Wald 95% confidence intervals (z = 1.96) are reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Of 286 households (median follow-up 304.50 days), 174 had an event. The exposure hazard ratio was 1.66 (95% CI 1.22 to 2.24, p = 0.001); the hazard ratio per year of age was 1.02.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
