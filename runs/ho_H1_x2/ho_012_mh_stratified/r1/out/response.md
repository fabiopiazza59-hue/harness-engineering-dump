# Run summary for ho_012_mh_stratified

Status: success
Reason: verification gate passed
Steps: 4; scripts: 1; gate attempts: 1; compactions: 0

## Claims
{
  "n_total": 445,
  "n_exposed": 223,
  "or_crude": 2.472192513368984,
  "or_mh": 2.500371270751079,
  "or_mh_ci_low": 1.2280032002095627,
  "or_mh_ci_high": 5.091075080692351,
  "mh_chi2": 21.432116859945058,
  "mh_p": 3.665790509810307e-06,
  "or_site1": 1.6607142857142858
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on all columns), keep first occurrence. 3. Replace -999 with NaN across all columns. 4. Filter to age between 18 and 80 inclusive (drop rows outside or missing age). 5. Normalize program: strip whitespace, lowercase. 6. Define exposed = program == 'tutoring', unexposed = program == 'standard' (drop other values if any). 7. Drop rows with missing event or site. 8. n_total = number of rows in final analysis sample; n_exposed = count of exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c) with a=exposed+event, b=exposed+noevent, c=unexposed+event, d=unexposed+noevent. 10. Build per-site 2x2 tables for sites 1-4, compute Mantel-Haenszel OR = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 11. Compute MH OR CI using Robins-Breslow-Greenland (RBG) method for variance of ln(OR_MH). 12. Compute MH chi-square with continuity correction: sum((|sum(a_i) - sum(E_i)| - 0.5)^2) / sum(Var_i) using standard hypergeometric formula. 13. Compute p-value from chi-square with df=1. 14. Compute site 1 OR directly from site1 2x2 table. 15. Output JSON with all claim slots.
