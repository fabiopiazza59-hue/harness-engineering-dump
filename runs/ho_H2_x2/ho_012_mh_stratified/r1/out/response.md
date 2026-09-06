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
1. Load data.csv. 2. Remove exact duplicate rows (identical on every column), keep first occurrence. 3. Replace -999 sentinel values with NaN across all columns. 4. Filter to age between 18 and 80 inclusive. 5. Normalise 'program' by trimming whitespace and lower-casing; define exposed = program contains 'tutoring', unexposed = 'standard' (or similar). 6. Drop rows with missing program, event, or site (needed for analysis) after sentinel replacement. 7. n_total = count of analysed rows; n_exposed = count exposed. 8. Build crude 2x2 table (exposed/unexposed x event/no event), compute crude OR = (a*d)/(b*c). 9. Stratify by site (1-4), build 2x2 tables per site, compute Mantel-Haenszel pooled OR = sum(a_i*d_i/n_i) / sum(b_i*c_i/n_i). 10. Compute MH OR CI using Robins-Breslow-Greenland (RBG) variance formula for log(OR_MH). 11. Compute MH chi-square with continuity correction: sum over strata of (|sum(a_i) - sum(E_i)| - 0.5)^2 / sum(Var_i), standard formula. 12. Compute p-value from chi2 distribution with 1 df. 13. Compute site 1 OR alone (a*d)/(b*c) for site==1 table. 14. Print all claims as JSON.
