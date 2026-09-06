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
1. Load data.csv.
2. Remove exact duplicate rows (identical on every column), keep first occurrence.
3. Replace -999 sentinel values with NaN across all columns.
4. Filter to age between 18 and 80 inclusive.
5. Drop rows with missing sbp_12w or sbp_12w_post (complete-case).
6. n_pairs = resulting row count.
7. mean_first = mean(sbp_12w), mean_second = mean(sbp_12w_post).
8. diff = sbp_12w_post - sbp_12w; mean_change = mean(diff); sd_change = sample SD (ddof=1) of diff.
9. Wilcoxon signed-rank test: two-sided, normal approximation (mode='approx'), no continuity correction, zero differences discarded (default behavior drops zeros) - use scipy.stats.wilcoxon(diff, zero_method='wilcox', correction=False, mode='approx').
10. w_stat = statistic, p_value = pvalue from that test.
11. cohens_dz = mean_change / sd_change.
12. pct_change per patient = (second-first)/first*100; mean_pct_change = mean of these values (over rows where first is nonzero/not missing, presumably all rows in sample since first already required non-missing).
13. Print JSON with all claim ids as last line of stdout.
