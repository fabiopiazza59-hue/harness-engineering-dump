# Run summary for fb_006_chisq

Status: success
Reason: verification gate passed
Steps: 9; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_unfertilised": 163,
  "n_fertilised": 135,
  "events_fertilised": 94,
  "prop_unfertilised": 0.4294478527607362,
  "prop_fertilised": 0.6962962962962963,
  "risk_ratio": 1.6213756613756614,
  "chi2_stat": 21.248013742781275,
  "p_value": 4.035283100798139e-06
}

## Plan
1. Load data.csv. 2. Exclude rows where age is missing or not in [18,80]. 3. Exclude rows with missing biomass (complete-case). 4. Group remaining rows by treatment into fertilised vs unfertilised. 5. Compute n_unfertilised, n_fertilised as group sizes. 6. Compute events_fertilised = sum(event==1) in fertilised group; events_unfertilised similarly. 7. Compute prop_fertilised = events_fertilised/n_fertilised; prop_unfertilised = events_unfertilised/n_unfertilised. 8. Compute risk_ratio = prop_fertilised/prop_unfertilised. 9. Build 2x2 contingency table (treatment x event) and run scipy.stats.chi2_contingency(correction=False) to get chi2_stat and p_value. 10. Print all claims as a single JSON object as last line of stdout.
