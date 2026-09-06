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
  "mh_chi2": 13.163890559094682,
  "mh_p": 0.00028539571090258065,
  "or_site1": 0.24107142857142858
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive (drop missing age). 5. Normalize diet: strip whitespace, lowercase. 6. Keep only rows with valid diet (mediterranean/usual) and valid event and site (drop missing needed vars). 7. n_total = count of analysed rows; n_exposed = count where diet=='mediterranean'. 8. Build 2x2 crude table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 9. Stratify by site (1-4), build 2x2 tables per site, compute MH pooled OR = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 10. Compute 95% CI for MH OR using Robins-Breslow-Greenland (RBG) variance formula. 11. Compute MH chi-square with continuity correction using standard formula: chi2 = (|sum(a_i) - sum(E_i)| - 0.5)^2 / sum(V_i), where E_i = row1*col1/n_i, V_i = hypergeometric variance. 12. p-value from chi2 with 1 df. 13. or_site1 = OR computed for site 1 stratum only. 14. Print JSON with all claim slots.
