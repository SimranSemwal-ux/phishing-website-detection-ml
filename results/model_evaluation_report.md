# Machine Learning Models & Evaluation Report
**Course**: Foundations of Data Science (FDS) Assignment 3

## 1. Executive Summary & Model Comparison Table

| Model                   |   Accuracy |   Precision (Phishing) |   Recall (Phishing) |   F1-Score (Phishing) |   ROC-AUC |   True_Positives (TP) |   False_Positives (FP) |   True_Negatives (TN) |   False_Negatives (FN) | Best_Hyperparameters                                                                     |
|:------------------------|-----------:|-----------------------:|--------------------:|----------------------:|----------:|----------------------:|-----------------------:|----------------------:|-----------------------:|:-----------------------------------------------------------------------------------------|
| Majority Class Baseline |     0.5568 |                 0      |              0      |                0      |    0.5    |                     0 |                      0 |                  1231 |                    980 | None (Baseline)                                                                          |
| Logistic Regression     |     0.9276 |                 0.9343 |              0.9    |                0.9168 |    0.9784 |                   882 |                     62 |                  1169 |                     98 | {'C': 1.0, 'solver': 'lbfgs'}                                                            |
| Decision Tree           |     0.9701 |                 0.9731 |              0.9592 |                0.9661 |    0.9778 |                   940 |                     26 |                  1205 |                     40 | {'criterion': 'entropy', 'max_depth': None, 'min_samples_split': 2}                      |
| Random Forest           |     0.9751 |                 0.9793 |              0.9643 |                0.9717 |    0.9964 |                   945 |                     20 |                  1211 |                     35 | {'max_depth': None, 'max_features': 'sqrt', 'min_samples_split': 2, 'n_estimators': 100} |

## 2. Metric Explanations for Viva Defense

- **Accuracy**: The overall fraction of correct predictions (both phishing and legitimate) among all evaluated websites: $\frac{TP + TN}{TP + TN + FP + FN}$. While useful for balanced datasets, it can be misleading under severe imbalance.
- **Precision (Phishing)**: Out of all websites the model flagged as phishing, what fraction actually was phishing: $\frac{TP}{TP + FP}$. High precision minimizes false alarms (False Positives), preventing benign websites from being mistakenly blocked.
- **Recall / Sensitivity (Phishing)**: Out of all real phishing websites in existence, what fraction was successfully detected by the model: $\frac{TP}{TP + FN}$. In cybersecurity, **Recall is the single most critical metric** because a False Negative (failing to catch a phishing site) allows an attacker to steal user credentials.
- **F1-Score**: The harmonic mean of precision and recall: $2 \cdot \frac{Precision \cdot Recall}{Precision + Recall}$. Balances both false alarms and missed threats into a single harmonic metric.
- **ROC-AUC**: Receiver Operating Characteristic Area Under the Curve evaluates the model's discriminative ability across every possible decision threshold from 0.0 to 1.0. A score of 0.5 indicates random guessing, while 1.0 represents perfect discrimination.

## 3. In-Depth Comparative Findings

- **Champion Model**: **Random Forest** achieved the highest overall performance with an Accuracy of **97.51%**, F1-Score of **0.9717**, and ROC-AUC of **0.9964**.
- **Baseline Comparison**: The Majority Baseline achieved 55.68% accuracy purely by predicting Legitimate for all cases, yielding a Recall of 0.0% for phishing. All three trained machine learning models dramatically outperformed the baseline by over 37-41 percentage points in accuracy.
- **Ensemble Advantage**: Random Forest reduced False Negatives compared to a single Decision Tree and Logistic Regression, confirming that bagging uncorrelated trees effectively suppresses overfitting and captures complex non-linear heuristic interactions.
