# Run summary for ho_011_paired

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_pairs": 220,
  "mean_first": 135.8531818181818,
  "mean_second": 130.93227272727273,
  "mean_change": -4.920909090909091,
  "sd_change": 5.726244881972723,
  "w_stat": 2586.5,
  "p_value": 1.1566676054660006e-23,
  "cohens_dz": -0.8593605743968481,
  "mean_pct_change": -3.651735354605737
}

## Plan
1. Load data.csv. 2. Drop exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows missing sbp_12w or sbp_12w_post. 6. Compute n_pairs = len(df). 7. mean_first = mean(sbp_12w), mean_second = mean(sbp_12w_post). 8. diff = sbp_12w_post - sbp_12w. mean_change = mean(diff), sd_change = sample SD (ddof=1). 9. Wilcoxon signed-rank test on diff, discard zeros, two-sided, normal approximation without continuity correction -> use scipy.stats.wilcoxon(diff, zero_method='wilcox', correction=False, mode='approx') to get statistic and p-value. 10. cohens_dz = mean_change/sd_change. 11. pct_change per patient = diff/sbp_12w*100, then mean_pct_change = mean of that. 12. Print JSON with all claims.
