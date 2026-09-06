# Run summary for dev_003_chisq

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_control": 135,
  "n_treatment": 134,
  "events_treatment": 34,
  "prop_control": 0.42962962962962964,
  "prop_treatment": 0.2537313432835821,
  "risk_ratio": 0.5905815748841997,
  "chi2_stat": 9.245980433811727,
  "p_value": 0.002360129010364937
}

## Plan
1. Load data.csv. 2. Apply exclusion: keep only age between 18 and 80 inclusive. 3. Apply exclusion: drop rows with missing sbp_12w (complete-case). 4. Group by arm (control vs treatment). 5. Compute n_control, n_treatment as group sizes. 6. Compute events_treatment = sum(event) in treatment group. 7. Compute prop_control = mean(event) in control group; prop_treatment = mean(event) in treatment group. 8. risk_ratio = prop_treatment / prop_control. 9. Build 2x2 contingency table (arm x event) and run scipy.stats.chi2_contingency with correction=False to get chi2_stat and p_value. 10. Print all claims as JSON.
