# Run summary for fb_009_mh_stratified

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_total": 313,
  "n_exposed": 167,
  "or_crude": 0.4149481314835646,
  "or_mh": 0.3925134629517352,
  "or_mh_ci_low": 0.23973798025231347,
  "or_mh_ci_high": 0.6426466863373705,
  "mh_chi2": 13.163890559094677,
  "mh_p": 0.00028539571090269167,
  "or_site1": 0.24107142857142858
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN in all measurement columns. 4. Filter age between 18-80 inclusive. 5. Normalize diet: strip whitespace, lowercase. 6. Drop rows missing age, diet, event, site (needed for analysis). 7. Define exposed = diet=='mediterranean'. 8. Build 2x2 table exposed/unexposed x event/no-event, compute crude OR. 9. Stratify by site (1-4), compute per-site 2x2 tables, compute MH pooled OR, MH chi-square with continuity correction, and 95% CI for MH OR (using Robins-Breslow-Day-Greenland variance formula or standard MH CI formula). 10. Compute site1-specific OR. 11. Output all claims as JSON.
