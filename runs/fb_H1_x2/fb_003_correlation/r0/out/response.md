# Run summary for fb_003_correlation

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_all": 219,
  "r_all": 0.5742298046885664,
  "p_all": 1.3109595005317223e-20,
  "n_caffeine": 105,
  "r_caffeine": 0.5709909340189405
}

## Plan
1. Load data.csv. 2. Exclude participants with age not in [18,80]. 3. Exclude rows with missing rt_ms. 4. Compute overall mean and sample SD (n-1) of rt_ms after above exclusions; remove rows where rt_ms more than 3 SD from mean. 5. Transform rt_ms: set values <1 to 1, then natural log. 6. Compute Spearman correlation between baseline and log_rt on full sample (n_all, r_all, p_all). 7. Subset to condition=='caffeine', compute Spearman correlation (n_caffeine, r_caffeine). 8. Print JSON with all claim ids.
