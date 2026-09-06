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
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows with missing math_score or math_score_post. 6. Compute n_pairs, mean_first (mean math_score), mean_second (mean math_score_post), diff = math_score_post - math_score, mean_change = mean(diff), sd_change = sample SD (ddof=1) of diff. 7. Paired t-test (scipy.stats.ttest_rel) -> t_stat, p_value. 8. Cohen's dz = mean_change/sd_change. 9. pct_change per subject = (post-first)/first*100, mean of these -> mean_pct_change. 10. Output JSON with all claims.
