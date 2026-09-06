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
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across all columns. 4. Filter age between 18 and 80 inclusive (drop missing age). 5. Normalize diet: strip whitespace, lower-case. 6. Define exposed = diet=='mediterranean', unexposed = diet=='usual' (or other label != mediterranean? Use only mediterranean vs usual, drop other/missing labels). 7. Build 2x2 table exposed/unexposed x event/no-event overall for crude OR (using cross-tab, standard odds ratio = (a*d)/(b*c)). 8. Compute per-site 2x2 tables (site 1-4) for MH pooled OR: OR_MH = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 9. Compute MH variance/CI via Robins-Breslow-Greenland method. 10. Compute MH chi-square with continuity correction (standard formula) and p-value from chi2 distribution df=1. 11. Compute OR for site 1 alone using standard 2x2 OR. 12. Output n_total, n_exposed, or_crude, or_mh, or_mh_ci_low/high, mh_chi2, mh_p, or_site1 as JSON.
