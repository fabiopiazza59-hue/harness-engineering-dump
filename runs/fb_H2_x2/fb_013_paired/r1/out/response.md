# Run summary for fb_013_paired

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_pairs": 211,
  "mean_first": 696.0663507109005,
  "mean_second": 672.70663507109,
  "mean_change": -23.359715639810425,
  "sd_change": 44.462565719883344,
  "t_stat": -7.631576452194591,
  "p_value": 7.993812952704315e-13,
  "cohens_dz": -0.5253793896415682,
  "mean_pct_change": -3.3764048264017363
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (all columns identical), keep first. 3. Replace -999 sentinel values with NaN across all columns. 4. Filter age between 18 and 80 inclusive. 5. Drop rows missing rt_ms or rt_ms_post. 6. n_pairs = count of remaining rows. 7. mean_first = mean(rt_ms), mean_second = mean(rt_ms_post). 8. diff = rt_ms_post - rt_ms; mean_change = mean(diff); sd_change = sample SD (ddof=1) of diff. 9. paired t-test: scipy.stats.ttest_rel(rt_ms_post, rt_ms) -> t_stat, p_value. 10. cohens_dz = mean_change / sd_change. 11. pct_change per subject = (rt_ms_post - rt_ms)/rt_ms*100, then mean_pct_change = mean of that. 12. Print all as JSON.
