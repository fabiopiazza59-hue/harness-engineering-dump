# Run summary for ho_003_correlation

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_all": 179,
  "r_all": 0.5927110676825217,
  "p_all": 2.320763149894151e-18,
  "n_tutoring": 83,
  "r_tutoring": 0.5951772454229052
}

## Plan
1. Load data.csv. 2. Exclude students with age outside [18,80]. 3. Exclude rows with missing math_score. 4. Compute mean and sample SD (n-1) of math_score on remaining data; remove rows where math_score is more than 3 SD from mean (outlier removal). 5. Transform math_score: set values <1 to 1, then natural log transform -> log_math_score. 6. Full sample: Spearman correlation between baseline and log_math_score, report n_all, r_all, p_all (two-sided). 7. Subset to program=='tutoring' (or similar) rows from analysis sample; compute Spearman correlation baseline vs log_math_score, report n_tutoring, r_tutoring. 8. Print JSON with all claims.
