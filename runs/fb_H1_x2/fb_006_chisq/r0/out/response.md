# Run summary for fb_006_chisq

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

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
1. Load data.csv. 2. Apply exclusions in order: (a) keep only age 18-80 inclusive; (b) drop rows with missing biomass. 3. Group by treatment (fertilised vs unfertilised). 4. Compute n per group, events per group (sum of event==1), proportions. 5. Compute risk ratio = prop_fertilised/prop_unfertilised. 6. Build 2x2 contingency table and run scipy.stats.chi2_contingency with correction=False to get chi2 stat and p-value. 7. Print JSON with all claim slots.
