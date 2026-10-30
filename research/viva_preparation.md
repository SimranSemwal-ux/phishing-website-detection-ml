# Viva Voce & Academic Defense Comprehensive Guide
**Project Title**: Phishing Website Detection Using Machine Learning and Statistical Analysis  
**Course**: Foundations of Data Science (FDS) Assignment 3  
**Student**: Simran Semwal | BTech Information Technology (2nd Year)  
**GitHub**: [SimranSemwal-ux/phishing-website-detection-ml](https://github.com/SimranSemwal-ux/phishing-website-detection-ml)

---

## 1. Project Overview from Beginning to End (Elevator Pitch)

> **How to explain this project in 2 minutes to the external examiner:**
> "Good morning, respected examiners. My project addresses one of the most critical vulnerabilities in cybersecurity: **Phishing attacks**, where fraudulent websites deceive users into exposing sensitive credentials and financial data. Because traditional URL blacklists suffer from zero-hour latency, we developed an intelligent, machine-learning-driven defense system using the **UCI Machine Learning Repository Phishing Websites Dataset (ID: 327)** comprising **11,055 instances and 30 heuristic features**.
>
> We executed an incremental 11-stage data science lifecycle:
> 1. **Data Ingestion & Integrity**: Fetched the pristine dataset using Python's `ucimlrepo` library, verifying 0 missing values and uncovering 64 conflicting feature combinations (label noise accounting for 3.2% of instances).
> 2. **Descriptive & Exploratory Analysis**: Computed comprehensive descriptive statistics across all 30 features and generated 6 publication-ready figures.
> 3. **Statistical Inference & Hypothesis Testing**: Conducted a Chi-Square Test of Independence on SSL/HTTPS certificate validity ($\chi^2 = 6,686.25, p < 0.0001$, Cramér's $V = 0.78$) and a non-parametric Mann-Whitney U test on URL length ($U = 1.57 \times 10^7, p < 0.0001$), formally validating that phishing and legitimate websites differ with statistical significance.
> 4. **Machine Learning & Tuning**: Built an 80:20 stratified split (8,844 train, 2,211 test) to prevent data leakage. Using 5-fold cross-validation on the training set, we tuned four models: Majority Baseline, Logistic Regression, Decision Tree, and Random Forest.
> 5. **Empirical Evaluation**: On unseen test data, our champion **Random Forest Classifier** achieved **97.51% Accuracy, 96.43% Recall (Phishing), and an extraordinary ROC-AUC of 0.9964**, outperforming the baseline by 41.8 percentage points.
> 6. **Interpretability**: Feature importance analysis proved that SSL certificate status and anchor URL ratios account for over 58% of predictive power."

---

## 2. Explanation of All 30 Dataset Features

Features are categorized into four standard domains:

### Category A: Address Bar Based Features (12)
1. **`having_ip_address`**: Legitimate sites use domain names (e.g., `google.com`). Attackers often use direct IP addresses (e.g., `http://192.168.1.1/login`) to bypass domain registration checks. (`-1`: IP used, `1`: Normal).
2. **`url_length`**: Phishers create excessively long URLs to hide the malicious domain in mobile browser address bars. (`1`: <54 chars, `0`: 54–75 chars, `-1`: >75 chars).
3. **`shortining_service`**: Shortening services (e.g., `bit.ly`, `tinyurl`) obscure the destination domain. (`-1`: Shortened, `1`: Normal).
4. **`having_at_symbol`**: Browsers ignore everything before `@` in a URL (e.g., `http://legit.com@evil.com` directs to `evil.com`). (`-1`: `@` present, `1`: Normal).
5. **`double_slash_redirecting`**: The `//` symbol should only appear after the protocol (`http://`). If `//` appears later in the path, it redirects the browser to a third-party host. (`-1`: Present after char 7, `1`: Normal).
6. **`prefix_suffix`**: Phishers insert hyphens (`-`) into domain names to mimic trusted brands (e.g., `paypal-update.com`). (`-1`: Hyphen present, `1`: Normal).
7. **`having_sub_domain`**: Excessive subdomain dots deceive users (e.g., `login.bank.secure.phish.com`). (`1`: 1 dot, `0`: 2 dots, `-1`: >2 dots).
8. **`sslfinal_state`**: Evaluates whether HTTPS is used, certificate issuer is trusted, and certificate age >= 1 year. (`1`: Valid HTTPS, `0`: Untrusted/short age, `-1`: No HTTPS).
9. **`domain_registration_length`**: Phishing domains are rarely registered for more than 1 year due to rapid takedowns. (`-1`: <= 1 year remaining, `1`: > 1 year).
10. **`favicon`**: A legitimate website serves its favicon from its own domain; phishing sites load favicons from external servers. (`-1`: External favicon, `1`: Internal).
11. **`port`**: Phishing servers frequently host rogue services on non-standard ports (e.g. 8080, 21, 666). (`-1`: Non-standard port open, `1`: Standard ports 80/443).
12. **`https_token`**: Attackers insert `https` inside the domain name (e.g., `http://https-bank.com`) to trick non-technical users. (`-1`: Present, `1`: Normal).

### Category B: Abnormal Request Based Features (6)
13. **`request_url`**: Checks what percentage of external objects (images, scripts, styles) are loaded from foreign domains. Legitimate sites host their own assets. (`1`: <22% external, `-1`: >=22%).
14. **`url_of_anchor`**: Measures the proportion of hyperlinks (`<a>`) pointing to `#`, `javascript:void(0)`, or external domains. Phishing landing pages disable navigation to prevent leaving the credential capture form. (`1`: <31%, `0`: 31–67%, `-1`: >67%).
15. **`links_in_tags`**: Percentage of `<meta>`, `<script>`, `<link>` pointing to external domains. (`1`: <17%, `0`: 17–81%, `-1`: >81%).
16. **`sfh` (Server Form Handler)**: The destination action of `<form action="...">`. If blank or `about:blank`, credentials are stolen via JavaScript. (`1`: Internal domain, `0`: External, `-1`: Blank/about:blank).
17. **`submitting_to_email`**: Use of `mailto:` functions to transmit stolen form entries directly to an attacker's inbox. (`-1`: `mailto:` present, `1`: Standard backend).
18. **`abnormal_url`**: The hostname does not match the WHOIS registration records. (`-1`: Abnormal, `1`: Normal).

### Category C: HTML & JavaScript Features (5)
19. **`redirect`**: Number of HTTP 301/302 redirects. Phishers chain redirects to bypass automated scanners. (`0`: <= 1 redirect, `1`: >= 2-4 redirects).
20. **`on_mouseover`**: JavaScript manipulates `window.status` when hovering over links to display a fake destination URL. (`-1`: Manipulated, `1`: Clean).
21. **`rightclick`**: JavaScript disables the right-click menu to prevent users from inspecting page source code. (`-1`: Disabled, `1`: Allowed).
22. **`popupwindow`**: Spawns fake modal dialogs demanding credential re-entry. (`-1`: Popup present, `1`: Normal).
23. **`iframe`**: Invisible or 0-pixel border `<iframe>` tags embedded to overlay malicious forms. (`-1`: Hidden iframe, `1`: None).

### Category D: Domain Based Features (7)
24. **`age_of_domain`**: Most phishing websites are younger than 6 months. (`-1`: < 6 months, `1`: >= 6 months).
25. **`dnsrecord`**: Whether the domain has a registered DNS host record. (`-1`: No DNS, `1`: Valid DNS).
26. **`web_traffic`**: High Alexa/SimilarWeb popularity indicates legitimate, established websites. (`1`: Top 100k, `0`: >100k, `-1`: Unranked).
27. **`page_rank`**: Google PageRank authority score. (`-1`: < 0.2, `1`: >= 0.2).
28. **`google_index`**: Legitimate sites are indexed by Google search crawlers; fleeting phishing pages are not. (`-1`: Not indexed, `1`: Indexed).
29. **`links_pointing_to_page`**: Inbound hyperlinks from other websites. (`1`: >2 links, `0`: 1–2 links, `-1`: 0 links).
30. **`statistical_report`**: Whether the host/IP appears on known threat intelligence blacklists (PhishTank, StopBadware). (`-1`: Blacklisted, `1`: Clean).

---

## 3. Explanation of Statistical Tests Used

### Test 1: Chi-Square Test of Independence ($\chi^2$)
- **Purpose**: Evaluates whether two categorical variables are independent or whether a statistically significant association exists between them.
- **Formula**: $\chi^2 = \sum \frac{(O - E)^2}{E}$, where $O$ is observed cell count and $E = \frac{(\text{Row Total})(\text{Column Total})}{N}$ is expected frequency under $H_0$.
- **Degrees of Freedom**: $df = (r - 1)(c - 1) = (3 - 1)(2 - 1) = 2$.
- **Effect Size (Cramér's V)**: $V = \sqrt{\frac{\chi^2}{N \cdot \min(r-1, c-1)}} = \sqrt{\frac{6686.25}{11055 \cdot 1}} = 0.7777$. A value above 0.5 denotes a very strong association.
- **Why applicable**: Both SSL state and target label are categorical variables, and all expected cell frequencies exceed 5.

### Test 2: Mann-Whitney U Test (Wilcoxon Rank-Sum Test)
- **Purpose**: Non-parametric test evaluating whether the probability of an observation from one population exceeding an observation from the second population differs from 0.5.
- **Why NOT Student's t-test?**: The `url_length` feature takes discrete values `{-1, 0, 1}` and severely violated normality (Shapiro-Wilk $p < 0.0001$). Applying a parametric t-test on non-normal, bounded ordinal data violates the normality assumption.
- **Result**: $U = 15,713,785.5$, $p = 2.06 \times 10^{-8} < 0.0001$.
- **Effect Size**: Rank-biserial correlation $r_{rb} = 1 - \frac{2U}{n_1 n_2} = -0.0421$.

### Test 3: Odds Ratio with Haldane-Anscombe Correction
- **Purpose**: Quantifies the odds of phishing given a domain hyphen vs no hyphen.
- **Correction**: In the $2 \times 2$ table, the cell for `prefix_suffix == 1` and `Phishing` was 0. Dividing by zero yields infinity. Adding $0.5$ to all four cells (Haldane-Anscombe) produces an asymptotically unbiased, finite odds ratio estimate.

---

## 4. Explanation of Machine Learning Algorithms

1. **Majority Class Baseline (Dummy Classifier)**:
   - Always outputs the majority class observed during training (`Legitimate`, 55.7%).
   - Serves as the scientific floor. Proves that accuracy alone is meaningless without precision, recall, and ROC-AUC.
2. **Logistic Regression**:
   - Models the log-odds of a website being phishing as a linear combination of input features: $\log\left(\frac{p}{1-p}\right) = \beta_0 + \sum \beta_i X_i$.
   - Uses L2 Ridge regularization ($C=1.0$) solved via the L-BFGS optimizer.
   - Provides transparent, interpretable weights (coefficients).
3. **Decision Tree Classifier**:
   - Recursively partitions the feature space into hyper-rectangles by choosing splits that maximize Information Gain / Shannon Entropy: $H(S) = -\sum p_i \log_2(p_i)$.
   - Captures non-linear decision thresholds without feature scaling.
4. **Random Forest Classifier**:
   - An ensemble bagging (Bootstrap Aggregation) algorithm that trains 100 deep decision trees on random bootstrap subsets of the data and random feature subspaces (`max_features='sqrt'`).
   - Final classification is determined by majority vote: $\hat{y} = \text{mode}(T_1(x), \dots, T_{100}(x))$.
   - Dramatically reduces variance and suppresses individual tree overfitting, resulting in 97.51% accuracy and 0.9964 ROC-AUC.

---

## 5. Explanation of Evaluation Metrics

- **Accuracy**: $\frac{TP + TN}{TP + TN + FP + FN}$ — overall correct rate.
- **Precision (Phishing)**: $\frac{TP}{TP + FP}$ — out of all sites predicted as phishing, how many were actually phishing. High precision prevents blocking safe sites.
- **Recall / Sensitivity (Phishing)**: $\frac{TP}{TP + FN}$ — out of all real phishing sites, how many were caught. **In cybersecurity, Recall is the most vital metric** because a False Negative means an attacker successfully tricks the user.
- **F1-Score**: $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ — harmonic mean balancing both errors.
- **ROC-AUC**: Evaluates True Positive Rate vs False Positive Rate across all thresholds. Score of 0.9964 demonstrates near-perfect discrimination.

---

## 6. Top 25 Viva Questions and Answers

### Q1: What is the main objective of your project?
**Answer**: To analyze website characteristics, discover statistical patterns discriminating phishing from legitimate sites, and develop machine learning models capable of automated real-time classification to protect users against credential theft.

### Q2: What dataset did you use and what are its key properties?
**Answer**: The UCI Phishing Websites dataset (ID: 327) by Mohammad et al. It contains 11,055 instances, 30 heuristic features, and a binary target (`result`: -1 for phishing, 1 for legitimate).

### Q3: Did you find any missing values?
**Answer**: No, the dataset has 0 missing values across all 30 features and the target.

### Q4: Did you find duplicate records, and why do they exist?
**Answer**: Yes, 5,206 exact duplicate rows exist (47.09%). This occurs because all 30 features are discrete heuristic bins (`{-1, 0, 1}`). Thousands of distinct URLs share identical heuristic profiles.

### Q5: What is "label noise" and did you find any in this dataset?
**Answer**: Yes. We discovered 64 distinct feature combinations representing 357 records (3.2%) that have identical input features but conflicting labels. This explains why no model can achieve 100% test accuracy on this feature space without overfitting.

### Q6: How did you split the dataset and why?
**Answer**: We used an 80:20 stratified train-test split (8,844 training, 2,211 testing) with `random_state=42`. Stratification ensures that the 55.7% / 44.3% class ratio is identical in both splits.

### Q7: How did you prevent data leakage?
**Answer**: Preprocessing mappings and 5-fold cross-validation hyperparameter tuning were conducted strictly on the training set. The test set of 2,211 instances remained completely unseen until final evaluation.

### Q8: What was your Majority Baseline accuracy and why did it fail?
**Answer**: It achieved 55.68% accuracy simply by predicting legitimate for all records. However, its Recall for phishing was 0.0%, meaning it caught zero phishing attacks. This highlights why accuracy is an insufficient metric in security.

### Q9: What hypothesis did you test for HTTPS/SSL status?
**Answer**: $H_0$: HTTPS status and website legitimacy are independent. $H_1$: They are dependent. We used a Chi-Square Test of Independence ($\chi^2 = 6,686.25, p < 0.0001, \text{Cramér's } V = 0.78$), decisively rejecting $H_0$.

### Q10: Why did you use the Mann-Whitney U test instead of a t-test for URL length?
**Answer**: `url_length` is a 3-level discrete ordinal feature (`-1, 0, 1`). The Shapiro-Wilk test yielded $p < 0.0001$, proving severe violation of normality. The parametric Student's t-test was invalid, making the non-parametric Mann-Whitney U test the correct statistical choice ($U = 1.57 \times 10^7, p < 0.0001$).

### Q11: What is Cramér's V and what does your result of 0.7777 mean?
**Answer**: Cramér's V measures the strength of association between categorical variables on a scale from 0 to 1. A value of 0.7777 represents an extraordinarily strong relationship between SSL certificate validity and website legitimacy.

### Q12: Why did you use the Haldane-Anscombe correction in Test 3?
**Answer**: In the $2 \times 2$ table of `prefix_suffix` vs class, one of the cells was zero (websites without hyphens had 0 phishing instances). Dividing by zero makes odds ratio undefined. Adding $0.5$ to each cell is the standard biostatistical correction.

### Q13: What machine learning models did you evaluate?
**Answer**: Majority Baseline, Regularized Logistic Regression, Decision Tree Classifier, and Random Forest Classifier.

### Q14: Which model performed the best and what were its metrics?
**Answer**: Random Forest Classifier:
- Accuracy: **97.51%**
- Precision (Phishing): **97.93%**
- Recall (Phishing): **96.43%**
- F1-Score (Phishing): **97.17%**
- ROC-AUC: **0.9964**

### Q15: How many False Negatives did Random Forest produce on the test set?
**Answer**: Only 35 False Negatives out of 980 real phishing websites in the test partition, compared to 98 False Negatives for Logistic Regression.

### Q16: Why is Recall more important than Precision in phishing detection?
**Answer**: A False Positive inconveniences a user by temporarily flagging a safe site. A False Negative allows the user to visit an active phishing site, potentially resulting in compromised bank accounts or identity theft.

### Q17: What are the top 3 most influential features in your Random Forest model?
**Answer**:
1. `sslfinal_state` (31.85% importance)
2. `url_of_anchor` (26.25% importance)
3. `web_traffic` (7.01% importance)
Together, SSL and Anchor URL explain over 58% of the model's decisions.

### Q18: What is Gini Impurity?
**Answer**: A measure of node misclassification risk: $Gini = 1 - \sum p_i^2$. Feature importance reflects the total reduction in Gini impurity brought by splits on that feature across all 100 trees.

### Q19: How does Random Forest prevent overfitting compared to a single Decision Tree?
**Answer**: A single tree grows deep and overfits training quirks. Random Forest uses bagging (bootstrap sampling) and random feature subsets to build 100 diverse, de-correlated trees, averaging their errors.

### Q20: What did the Logistic Regression coefficients reveal?
**Answer**: Negative coefficients for `sslfinal_state` and `url_of_anchor` heavily decrease the log-odds of phishing, confirming that valid SSL and internal anchors predict legitimate sites.

### Q21: What is the ROC curve and what does an AUC of 0.9964 indicate?
**Answer**: It plots True Positive Rate against False Positive Rate across all classification thresholds. An AUC of 0.9964 indicates that a randomly chosen phishing site has a 99.64% probability of receiving a higher phishing risk score than a randomly chosen legitimate site.

### Q22: What are the primary limitations of this dataset?
**Answer**: Features are pre-computed discrete indicators (`{-1, 0, 1}`) rather than raw URLs or DOM trees, and the dataset does not include contemporary evasion tactics like QR code phishing (quishing) or multi-factor authentication adversary-in-the-middle proxies.

### Q23: How would this model be deployed in a production environment?
**Answer**: As a lightweight Chrome/Firefox browser extension that extracts the 30 heuristic features upon navigation and queries an ONNX or serialized Random Forest microservice via WebAssembly for sub-10-millisecond inference.

### Q24: What future improvements would you propose?
**Answer**: Incorporating raw URL sequence embeddings via transformer models (BERT), adding real-time visual similarity screenshots using convolutional networks, and active learning pipelines that ingest newly reported PhishTank URLs daily.

### Q25: Why did you choose this topic for Foundations of Data Science?
**Answer**: Because cybersecurity phishing detection represents an authentic, high-impact societal problem where data science directly protects human privacy and assets, allowing us to combine data cleaning, descriptive statistics, inferential hypothesis testing, and machine learning into a unified, actionable project.
