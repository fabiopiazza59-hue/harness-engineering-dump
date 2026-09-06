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
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 with NaN across all columns (sentinel missing). 4. Filter age between 18 and 80 inclusive. 5. Drop rows missing sbp_12w or sbp_12w_post. 6. This is the analysis sample; n_pairs = count. 7. mean_first = mean(sbp_12w), mean_second = mean(sbp_12w_post). 8. diff = sbp_12w_post - sbp_12w (second minus first). mean_change = mean(diff), sd_change = sample SD (ddof=1) of diff. 9. Wilcoxon signed-rank test: two-sided, normal approximation (mode='approx'), no continuity correction (correction=False), zero differences discarded (zero_method='wilcox' default drops zeros). Use scipy.stats.wilcoxon with correction=False, mode='approx', zero_method='wilcox'. w_stat = statistic, p_value = pvalue. 10. cohens_dz = mean_change / sd_change. 11. pct_change per patient = (second-first)/first*100, then mean_pct_change = mean of these (over analysis sample, using first as sbp_12w, before dropping zero diffs - note Wilcoxon drops zeros only for test statistic, not for other stats). 12. Output all in JSON.
