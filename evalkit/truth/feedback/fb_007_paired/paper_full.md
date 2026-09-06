# Within-student change in end-of-year mathematics score between two assessments

## Abstract

Background: A cohort study of a peer-tutoring program in secondary schools. Methods: The change in end-of-year mathematics score (0-100) from the first to the second assessment was tested with a paired t-test (two-sided). Results: see the Results section. Conclusion: the findings are discussed in the context of the analysis sample.

## Introduction

We report a cohort study of a peer-tutoring program in secondary schools. The primary question concerns enrolment in the peer-tutoring program and end-of-year mathematics score (0-100). The accompanying dataset (data.csv) contains one row per student-record as exported from the study database, including some duplicated exports and sentinel-coded missing values; it is described in the data dictionary.

## Methods

**Participants and data.** The export contains 265 records. Variables are listed in the data dictionary. Group membership is recorded in `program`.

**Data cleaning and exclusions.** Exact duplicate records (identical on every column) were removed, keeping the first occurrence. The value -999 denotes a missing measurement and was treated as missing. Only students aged 18 to 80 years inclusive were analysed. Records with missing math_score, math_score_post were excluded (complete-case analysis).

**Statistical analysis.** The change in end-of-year mathematics score (0-100) from the first to the second assessment was tested with a paired t-test (two-sided). The mean change is the mean of (second minus first) over analysed students; its standard deviation is the sample SD of the paired differences. Cohen's dz is the mean change divided by the SD of the differences. Percent change was computed per student as (second - first) / first x 100 and then averaged. All analyses used the cleaned analysis sample; no random resampling was used.

## Results

Among 223 students the mean value changed from 65.10 to 68.35, a mean change of 3.25 (SD 6.53; statistic = 7.43, p < 0.001; dz = 0.498); the mean percent change was 5.33%.

## Discussion

The analysis followed the pre-specified plan. Limitations include reliance on database exports and complete-case handling of missing values.
