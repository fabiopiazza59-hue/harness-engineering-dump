# Time to the study event by enrolment in the peer-tutoring program: a survival analysis

## Abstract

Background: A cohort study of a peer-tutoring program in secondary schools. Methods: Follow-up time in days was computed from the enrolment date to the date of event or last contact. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a cohort study of a peer-tutoring program in secondary schools. The primary question concerns enrolment in the peer-tutoring program and end-of-year mathematics score (0-100). The accompanying dataset (data.csv) contains one row per student-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 424 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only students aged 18 to 80 years inclusive were analysed. Group labels in `program` were entered free-text and were normalised by trimming whitespace and lower-casing before use.

**Statistical analysis.** Follow-up time in days was computed from the enrolment date to the date of event or last contact. Follow-up was administratively censored at 730 days: students with longer follow-up were censored at 730 days and counted as event-free, and records with zero follow-up were excluded. The hazard of the study event was modelled with a Cox proportional-hazards model with enrolment in the peer-tutoring program (1 = tutoring, 0 = standard) and age (years) as covariates, using the Breslow method for ties. Hazard ratios with Wald 95% confidence intervals (z = 1.96) are reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Of [n_model] students (median follow-up [median_followup_days] days), [n_events] had an event. The exposure hazard ratio was [hr_exposure] (95% CI [hr_ci_low] to [hr_ci_high], p [p_exposure]); the hazard ratio per year of age was [hr_age].

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_model`: Number of students in the Cox model
- `n_events`: Number of events after censoring
- `median_followup_days`: Median follow-up time in days (all analysed records, after censoring)
- `hr_exposure`: Hazard ratio for the exposure
- `hr_ci_low`: Lower 95% CI of the exposure hazard ratio
- `hr_ci_high`: Upper 95% CI of the exposure hazard ratio
- `p_exposure`: p-value of the exposure term
- `hr_age`: Hazard ratio per year of age

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
