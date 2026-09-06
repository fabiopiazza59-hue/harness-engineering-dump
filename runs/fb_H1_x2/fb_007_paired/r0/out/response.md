# Run summary for fb_007_paired

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_pairs": 223,
  "mean_first": 65.10448430493273,
  "mean_second": 68.35291479820629,
  "mean_change": 3.248430493273543,
  "sd_change": 6.525900217723114,
  "t_stat": 7.433367098484354,
  "p_value": 2.2731876609542747e-12,
  "cohens_dz": 0.4977750785173543,
  "mean_pct_change": 5.3254985544727775
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows missing math_score or math_score_post. 6. n_pairs = resulting row count. 7. mean_first = mean(math_score), mean_second = mean(math_score_post). 8. diff = math_score_post - math_score; mean_change = mean(diff); sd_change = sample SD (ddof=1) of diff. 9. paired t-test (scipy ttest_rel) two-sided -> t_stat, p_value. 10. cohens_dz = mean_change / sd_change. 11. pct_change = diff/math_score*100 per subject, then mean -> mean_pct_change. 12. Print all as JSON.
