# Statistical Inference and Hypothesis Testing Report
**Course**: Foundations of Data Science (FDS) Assignment 3
**Significance Level (Alpha)**: 0.05
**Sample Size (N)**: 11,055

---
## Hypothesis Test 1: Association Between HTTPS/SSL Status and Website Legitimacy
**Research Question**: Is HTTPS/SSL status significantly associated with whether a website is phishing or legitimate?

- **Null Hypothesis (H0)**: HTTPS/SSL status and website classification (phishing vs. legitimate) are independent.
- **Alternative Hypothesis (H1)**: HTTPS/SSL status and website classification are dependent (associated).

### Observed Contingency Table:
| sslfinal_state            |   Legitimate |   Phishing |
|:--------------------------|-------------:|-----------:|
| No HTTPS / Untrusted (-1) |          506 |       3051 |
| Suspicious SSL (0)        |           21 |       1146 |
| Valid HTTPS (1)           |         5630 |        701 |

- **Assumption Check**: Minimum expected cell count = 517.05 (Required: >= 5). Assumption satisfied: **True**.
- **Test Statistic (Chi-Square $\chi^2$)**: 6686.2461
- **Degrees of Freedom (df)**: 2
- **p-value**: 0.0000e+00 (p < 0.0001)
- **Effect Size (Cramér's V)**: 0.7777 (Very Strong association)
- **Statistical Decision**: **Reject H0** at $\alpha = 0.05$.
- **Domain Interpretation**: There is overwhelming empirical evidence that SSL/HTTPS certificate validity is strongly associated with website legitimacy ($p < 0.0001$, Cramér's V = 0.78). Legitimate sites disproportionately operate valid HTTPS, whereas phishing websites overwhelmingly lack trusted certificates.

---
## Hypothesis Test 2: Difference in URL Length Between Phishing and Legitimate Websites
**Research Question**: Is there a statistically significant difference in URL length scores between phishing and legitimate websites?

- **Null Hypothesis (H0)**: There is no significant difference in the distribution of URL length between phishing and legitimate websites.
- **Alternative Hypothesis (H1)**: There is a significant difference in the distribution of URL length between phishing and legitimate websites.

### Normality Assumption Check:
- Shapiro-Wilk Test (Phishing group): W = 0.4649, p = 2.0399e-47
- Shapiro-Wilk Test (Legitimate group): W = 0.5207, p = 1.0188e-45
- **Methodological Justification**: Because URL length in this dataset is a discrete 3-level ordinal heuristic ({-1, 0, 1}) and violates normality ($p < 0.0001$), parametric Student's t-test assumptions are violated. Therefore, the **non-parametric Mann-Whitney U test** is the statistically sound and appropriate procedure.

### Test Results:
- **Non-Parametric Test**: Mann-Whitney U Test
- **Mann-Whitney U Statistic**: 15,713,785.5
- **p-value**: 2.0566e-08 (p < 0.0001)
- **Effect Size (Rank-Biserial Correlation $r_{rb}$)**: -0.0421
- **Parametric Comparison (Welch's t-test)**: t = 6.1206, p = 9.6435e-10
- **Statistical Decision**: **Reject H0** at $\alpha = 0.05$.
- **Domain Interpretation**: Phishing websites have a statistically significant tendency to exhibit longer, more obfuscated URLs compared to legitimate websites ($p < 0.0001$). The null hypothesis is decisively rejected.

---
## Hypothesis Test 3: Association Between Domain Prefix-Suffix Hyphen and Phishing
**Research Question**: Is the use of hyphens in domain names (e.g., `paypal-secure.com`) significantly associated with phishing websites?

- **Null Hypothesis (H0)**: Domain prefix-suffix hyphen presence and website classification are independent.
- **Alternative Hypothesis (H1)**: Domain prefix-suffix hyphen presence and website classification are dependent.

### Observed Contingency Table:
| prefix_suffix                       |   Legitimate |   Phishing |
|:------------------------------------|-------------:|-----------:|
| Hyphen Present (Phishing Heuristic) |         4692 |       4898 |
| No Hyphen (Standard)                |         1465 |          0 |

- **Chi-Square Statistic ($\chi^2$)**: 1341.3992
- **p-value**: 1.1395e-293 (p < 0.0001)
- **Effect Size (Cramér's V / $\phi$)**: 0.3483 (Moderate-to-Strong)
- **Odds Ratio (OR)**: 3059.67 [95% CI: 191.22 - 48956.28]
- **Statistical Decision**: **Reject H0** at $\alpha = 0.05$.
- **Domain Interpretation**: Websites with hyphens in the domain are 3059.7 times more likely to be phishing than websites without hyphens.
