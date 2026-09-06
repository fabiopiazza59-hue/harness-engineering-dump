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
1. Load data.csv. 2. Apply exclusions in order: filter age 18-80 inclusive; drop rows with missing sbp_12w. 3. Group by arm (control/treatment). 4. Compute n per group, events per group (event==1), proportions. 5. Compute risk ratio = prop_treatment/prop_control. 6. Run Pearson chi-square test of independence (2x2 table arm x event) without continuity correction (scipy.stats.chi2_contingency correction=False). 7. Output all claim values as JSON.
