# LinkedIn Showcase Content: Phishing Website Detection
**Author**: Simran Semwal  
**Repository**: [https://github.com/SimranSemwal-ux/phishing-website-detection-ml](https://github.com/SimranSemwal-ux/phishing-website-detection-ml)

---

## Part A: LinkedIn Profile — "Projects" Section Entry

### **Project Title**
**Phishing Website Detection Using Machine Learning and Statistical Analysis**

### **Dates**
October 2026 – Present

### **Associated With**
BTech in Information Technology | Foundations of Data Science (FDS)

### **Project URL**
`https://github.com/SimranSemwal-ux/phishing-website-detection-ml`

### **Description**
Developed an end-to-end, academic-grade cybersecurity data science framework to detect zero-hour phishing websites utilizing the official **UCI Machine Learning Repository Phishing Websites Dataset (ID: 327)** comprising **11,055 instances and 30 heuristic features**.

**Key Achievements & Engineering Highlights:**
- **Statistical Inference & Hypothesis Testing**: Conducted a Chi-Square Test of Independence on SSL/HTTPS certificate authenticity ($\chi^2 = 6,686.25, p < 0.0001, \text{Cramér's } V = 0.78$) and a non-parametric Mann-Whitney U test on URL length distributions ($U = 1.57 \times 10^7, p < 0.0001$), formally proving statistical significance before modeling.
- **Data Engineering & Leakage Prevention**: Handled discrete ordinal feature spaces, audited 64 conflicting feature combinations (label noise), and enforced a strictly stratified 80:20 train-test split (8,844 train / 2,211 test) with zero data leakage.
- **Machine Learning Architecture**: Implemented and benchmarked 4 algorithms under 5-fold cross-validation: Majority Dummy Baseline, Regularized Logistic Regression, Decision Tree, and Random Forest Ensemble.
- **Empirical Champion Performance**: Our tuned **Random Forest Classifier** achieved **97.51% Accuracy, 97.93% Precision, 96.43% Recall (Phishing), and an ROC-AUC of 0.9964** on unseen test data, minimizing catastrophic False Negatives to just 35 out of 980 phishing samples.
- **Model Explainability**: Extracted Gini importance and logistic odds weights, demonstrating that SSL Final State (31.9%) and URL of Anchor (26.3%) account for >58% of classification decisions.

### **Skills Used**
Machine Learning · Statistical Hypothesis Testing · Data Cleaning & Preprocessing · Python (Pandas, NumPy, Scikit-learn, SciPy) · Exploratory Data Analysis · Data Visualization (Matplotlib, Seaborn) · Git & GitHub · Cybersecurity Analytics

---

## Part B: LinkedIn Announcement Post

```markdown
🚀 Excited to share my latest end-to-end Data Science & Cybersecurity project: "Phishing Website Detection Using Machine Learning and Statistical Analysis"! 🛡️💻

With zero-hour phishing attacks accounting for billions in annual cyber losses, traditional URL blacklists struggle to keep pace with evasive domains. For my Foundations of Data Science (FDS) assignment, I wanted to go beyond simple model training and build an authentic, statistically grounded investigation into what makes a website fraudulent.

Using the official UCI Machine Learning Repository dataset (11,055 websites, 30 features), here is what I engineered:

📊 1. Statistical Hypothesis Testing
Before jumping into machine learning, I wanted to mathematically test core security assumptions:
• Chi-Square Test of Independence on HTTPS/SSL Status: Demonstrated a massive association (chi2 = 6,686.25, p < 0.0001, Cramér's V = 0.78) with website legitimacy.
• Mann-Whitney U Test on URL Length: Formally tested normality (violating Shapiro-Wilk) and proved with non-parametric significance (p = 2.06e-8) that phishing URLs are systematically longer and more obfuscated.

🧹 2. Data Cleaning & Integrity
• Audited all 30 features, confirming 0 missing values across the 11,055 records.
• Uncovered 64 conflicting feature combinations (357 rows, ~3.2% label noise), mathematically proving why ~97.5% test accuracy represents the empirical Bayes optimal boundary for this feature space!
• Designed a strict 80:20 stratified split (8,844 train, 2,211 test) to guarantee zero data leakage.

🤖 3. Machine Learning & Model Evaluation
Benchmarked four algorithms tuned with 5-fold cross-validation:
• Majority Baseline: 55.68% Accuracy (0.0% Phishing Recall — caught zero attacks!)
• Logistic Regression: 92.76% Accuracy | 90.00% Recall | 0.9784 ROC-AUC
• Decision Tree: 97.01% Accuracy | 95.92% Recall | 0.9778 ROC-AUC
• 🏆 Random Forest Classifier: 97.51% Accuracy | 96.43% Recall | 97.93% Precision | 0.9964 ROC-AUC!

In cybersecurity, Recall is the most critical metric because a False Negative means an attacker successfully tricks a victim. Random Forest minimized False Negatives to just 35 out of 980 phishing sites on completely unseen test data.

🔍 4. Interpretability
Gini importance proved that SSL Certificate Validity (31.9%) and Anchor URL ratios (26.3%) drive over 58% of all classification decisions.

📁 The complete open-source repository—including modular Python scripts, high-resolution plots, statistical reports, and an extensive literature review—is live on GitHub:
👉 https://github.com/SimranSemwal-ux/phishing-website-detection-ml

A huge thank you to my professors and peers for their continuous feedback. Looking forward to your thoughts and suggestions in the comments! 👇

#DataScience #MachineLearning #Cybersecurity #Python #InformationTechnology #ArtificialIntelligence #Statistics #ScikitLearn #PhishingDetection #StudentProjects #BTech #OpenSource
```
