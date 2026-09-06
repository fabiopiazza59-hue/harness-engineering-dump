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
1. Load data.csv. 2. Apply age filter: keep age between 18 and 80 inclusive. 3. Drop rows with missing math_score. 4. Compute mean and sample SD (n-1) of math_score on remaining data; remove rows where math_score is more than 3 SD from mean. 5. Log-transform math_score: clip values <1 to 1, then natural log. 6. Compute Spearman correlation between baseline and log(math_score) for full sample -> n_all, r_all, p_all. 7. Subset to program=='tutoring' rows, compute Spearman correlation -> n_tutoring, r_tutoring. 8. Print JSON with all claims.
