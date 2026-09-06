# Site-stratified association between enrolment in the peer-tutoring program and the study event

## Abstract

Background: A cohort study of a peer-tutoring program in secondary schools. Methods: The association between enrolment in the peer-tutoring program (exposed = tutoring) and the study event was summarised with the crude odds ratio and with the Mantel-Haenszel odds ratio pooled across the four study sites (2x2 tables ordered exposed/unexposed by event/no event), with its 95% confidence interval, and the Mantel-Haenszel chi-square test with continuity correction. Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a cohort study of a peer-tutoring program in secondary schools. The primary question concerns enrolment in the peer-tutoring program and end-of-year mathematics score (0-100). The accompanying dataset (data.csv) contains one row per student-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 463 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only students aged 18 to 80 years inclusive were analysed. Group labels in `program` were entered free-text and were normalised by trimming whitespace and lower-casing before use.

**Statistical analysis.** The association between enrolment in the peer-tutoring program (exposed = tutoring) and the study event was summarised with the crude odds ratio and with the Mantel-Haenszel odds ratio pooled across the four study sites (2x2 tables ordered exposed/unexposed by event/no event), with its 95% confidence interval, and the Mantel-Haenszel chi-square test with continuity correction. The site-specific odds ratio for site 1 is also reported. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among [n_total] students ([n_exposed] exposed) the crude odds ratio was [or_crude] and the Mantel-Haenszel odds ratio pooled over sites was [or_mh] (95% CI [or_mh_ci_low] to [or_mh_ci_high]; MH chi-square = [mh_chi2], p [mh_p]). Within site 1 the odds ratio was [or_site1].

Numeric results are withheld in this view. The quantities to reproduce are listed as claim slots in task.json; each slot id appears where the value would be reported.

Claim slots:
- `n_total`: Number of students analysed
- `n_exposed`: Number in the tutoring (exposed) group
- `or_crude`: Crude odds ratio (exposed vs unexposed)
- `or_mh`: Mantel-Haenszel pooled odds ratio across sites
- `or_mh_ci_low`: Lower 95% CI of the MH odds ratio
- `or_mh_ci_high`: Upper 95% CI of the MH odds ratio
- `mh_chi2`: Mantel-Haenszel chi-square statistic (continuity corrected)
- `mh_p`: p-value of the Mantel-Haenszel test
- `or_site1`: Odds ratio within site 1

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
