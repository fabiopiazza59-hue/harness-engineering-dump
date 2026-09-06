# Run summary for fb_009_mh_stratified

Status: success
Reason: verification gate passed
Steps: 6; scripts: 2; gate attempts: 2; compactions: 0

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
1. Load data.csv. 2. Remove exact duplicate rows (identical on all columns), keep first occurrence. 3. Replace -999 sentinel values with NaN across all columns. 4. Filter to age between 18 and 80 inclusive. 5. Normalize diet: strip whitespace, lowercase. 6. Define exposed = diet=='mediterranean', unexposed = diet=='usual' (drop other/missing diet values). 7. Handle missing event similarly (drop missing event rows, complete-case). 8. n_total = count of analysed rows; n_exposed = count exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 10. Build per-site 2x2 tables (site 1-4), compute Mantel-Haenszel OR = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 11. Compute 95% CI for MH OR using Robins-Breslow-Greenland (RBG) variance estimator, standard approach. 12. Compute MH chi-square with continuity correction using standard formula: chi2 = (|sum(a_i) - sum(E_i)| - 0.5)^2 / sum(Var_i), then p-value from chi2 distribution df=1. 13. Compute OR for site 1 alone. 14. Print all claims as JSON.
