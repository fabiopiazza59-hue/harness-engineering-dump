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
1. Load data.csv. 2. Exclude students with age <18 or >80 (inclusive range 18-80 kept). 3. Exclude rows with missing math_score. 4. Compute mean and sample SD (n-1) of math_score on remaining data; remove outliers >3 SD from mean. 5. Transform math_score: set values <1 to 1, then natural log. 6. Full sample: Spearman correlation between baseline and log_math_score, get r and two-sided p-value, n_all = sample size. 7. Subset to program=='tutoring' (check exact label), compute Spearman correlation r_tutoring, n_tutoring = sample size. 8. Print all results as JSON.
