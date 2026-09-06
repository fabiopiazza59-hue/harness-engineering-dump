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
1. Load data.csv (212 rows). 2. Exclude students with age not in [18,80]. 3. Exclude rows with missing math_score. 4. Compute mean and sample SD (n-1) of math_score on remaining data; remove rows where math_score is more than 3 SD from mean (outliers). 5. Transform math_score: set values <1 to 1, then natural log transform -> log_math_score. 6. Full sample: compute Spearman correlation between baseline and log_math_score, get r_all, p_all, n_all = len(df). 7. Subset to program == 'tutoring' (check unique values of program column), compute Spearman correlation between baseline and log_math_score within that group -> r_tutoring, n_tutoring. 8. Print JSON with all claims.
