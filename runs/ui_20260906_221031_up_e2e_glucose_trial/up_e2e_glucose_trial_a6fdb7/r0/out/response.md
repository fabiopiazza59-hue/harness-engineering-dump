# Run summary for up_e2e_glucose_trial_a6fdb7

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_total_collected": 350,
  "n_usual": 151,
  "n_mediterranean": 161,
  "mean_glucose_usual": 102.70132450331126,
  "mean_glucose_mediterranean": 98.29689440993788,
  "sd_glucose_mediterranean": 13.055125537314112,
  "mean_difference": -4.404430093373378,
  "t_statistic": -2.9669917233423937,
  "p_value": 0.003241289877945753,
  "cohens_d": -0.3361183478602517
}

## Plan
1. Load data.csv, count rows -> n_total_collected. 2. Apply exclusions in order: (a) keep age between 18 and 80 inclusive; (b) drop rows with missing glucose_fu; (c) compute overall mean and sample SD (n-1) of glucose_fu on this filtered set, then remove rows where |glucose_fu - mean| > 3*SD. 3. On remaining analysis sample, split by diet column into 'usual' and 'mediterranean' groups, get n per group. 4. Compute mean and sample SD (n-1) of glucose_fu for each group. 5. Compute mean_difference = mean(mediterranean) - mean(usual). 6. Run scipy.stats.ttest_ind(mediterranean, usual, equal_var=True) for t_statistic and p_value. 7. Compute pooled SD = sqrt(((n1-1)*sd1^2+(n2-1)*sd2^2)/(n1+n2-2)) and cohens_d = mean_difference/pooled_SD. 8. Print all claims as JSON.
