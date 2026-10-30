# Exploratory Data Analysis & Visualizations Interpretation Guide

### Graph 1: Class Distribution (`01_class_distribution.png`)
- **X-axis**: Website Classification (Legitimate vs Phishing)
- **Y-axis**: Number of Websites
- **Interpretation**: Legitimate websites comprise 6,157 instances (55.7%), while phishing websites account for 4,898 instances (44.3%). The class balance ratio is 1.26:1. This represents a healthy, balanced binary distribution, confirming that accuracy and ROC-AUC are reliable metrics and extreme synthetic balancing techniques (e.g. SMOTE) are not mandatory.

### Graph 2: URL Length Distribution (`02_url_length_distribution.png`)
- **X-axis**: URL Length Category (-1: >75 chars, 0: 54-75 chars, 1: <54 chars)
- **Y-axis**: Count of Websites
- **Interpretation**: Legitimate websites predominantly feature short, concise URLs (<54 chars). In contrast, phishing websites exhibit a noticeably higher propensity for long URLs (>75 characters) to obscure the true domain destination and deceive visitors.

### Graph 3: Comparative Boxplots (`03_feature_boxplots.png`)
- **Subplots**: SSL State, URL of Anchor, Subdomains, Prefix-Suffix.
- **Interpretation**: Phishing sites cluster heavily at negative values (-1) for SSL final state and URL of Anchor, demonstrating a strong lack of trusted certificates and heavy reliance on empty or external anchor links.

### Graph 4: Correlation Heatmap (`04_correlation_heatmap.png`)
- **Interpretation**: The strongest positive correlations with legitimate status are `sslfinal_state` (r = +0.71) and `url_of_anchor` (r = +0.69). Features like `prefix_suffix` (r = +0.35) and `web_traffic` (r = +0.35) also demonstrate substantial linear and monotonic association with legitimate websites.

### Graph 5: Multi-Feature Heuristic Comparison (`05_feature_comparison_by_class.png`)
- **Interpretation**: Highlights the stark contrast in heuristic compliance. Over 85% of legitimate websites possess valid SSL and safe anchor links, compared to less than 20% of phishing websites.

### Graph 6: SSL/TLS State Breakdown (`06_ssl_state_vs_target.png`)
- **Interpretation**: Demonstrates that absence of HTTPS or untrusted certificates is one of the single most decisive indicators of phishing activity.
