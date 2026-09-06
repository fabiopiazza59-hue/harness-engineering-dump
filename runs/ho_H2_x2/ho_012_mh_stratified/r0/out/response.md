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
  "or_mh_ci_low": 1.7048032099066308,
  "or_mh_ci_high": 3.6672012671420107,
  "mh_chi2": 21.432116859945058,
  "mh_p": 3.665790509810307e-06,
  "or_site1": 1.6607142857142858
}

## Plan
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 with NaN across all columns. 4. Filter to age between 18 and 80 inclusive (drop missing age too). 5. Normalize program: strip whitespace, lowercase. 6. Define exposed = program=='tutoring', unexposed = program=='standard' (drop other/missing labels). 7. Drop rows with missing event or site. 8. n_total = count of analysis sample; n_exposed = count exposed. 9. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 10. Stratify by site (1-4), build 2x2 tables per site, compute MH pooled OR = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 11. Compute 95% CI for MH OR using Robins-Breslow-Day-Greenland variance formula. 12. Compute MH chi-square with continuity correction (standard formula: (|sum(a_i) - sum(E_i)| - 0.5)^2 / sum(Var_i)), and p-value from chi2 distribution df=1. 13. Compute site1 OR directly from site1 2x2 table. 14. Print all claims as JSON.
