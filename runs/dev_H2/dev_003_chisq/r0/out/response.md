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
1. Load data.csv. 2. Apply exclusions in order: (a) keep age between 18 and 80 inclusive, (b) drop rows with missing sbp_12w. 3. Compute n per arm (control/treatment) from arm column. 4. Compute events per arm from event column (sum of event==1). 5. Compute proportions = events/n per arm. 6. Compute risk ratio = prop_treatment/prop_control. 7. Build 2x2 contingency table (arm x event) and run scipy.stats.chi2_contingency with correction=False to get chi2 stat and p-value (Pearson chi-square, no continuity correction). 8. Output all claims as JSON.
