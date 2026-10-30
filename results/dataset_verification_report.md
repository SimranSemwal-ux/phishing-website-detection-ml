# UCI Phishing Websites Dataset (ID: 327) - Ingestion & Verification Report

- **DOI**: [10.24432/C51W2X](https://doi.org/10.24432/C51W2X)
- **Total Instances**: 11,055
- **Total Features**: 30
- **Target Column**: `result`
- **Class Counts**: Class `-1` (Phishing): 4,898 (44.31%), Class `1` (Legitimate): 6,157 (55.69%)
- **Missing Values**: 0
- **Exact Duplicates**: 5206

## Feature Inventory

| # | Feature Name | Data Type | Unique Values |
|---|---|---|---|
| 1 | `having_ip_address` | int64 | [-1, 1] |
| 2 | `url_length` | int64 | [-1, 0, 1] |
| 3 | `shortining_service` | int64 | [-1, 1] |
| 4 | `having_at_symbol` | int64 | [-1, 1] |
| 5 | `double_slash_redirecting` | int64 | [-1, 1] |
| 6 | `prefix_suffix` | int64 | [-1, 1] |
| 7 | `having_sub_domain` | int64 | [-1, 0, 1] |
| 8 | `sslfinal_state` | int64 | [-1, 0, 1] |
| 9 | `domain_registration_length` | int64 | [-1, 1] |
| 10 | `favicon` | int64 | [-1, 1] |
| 11 | `port` | int64 | [-1, 1] |
| 12 | `https_token` | int64 | [-1, 1] |
| 13 | `request_url` | int64 | [-1, 1] |
| 14 | `url_of_anchor` | int64 | [-1, 0, 1] |
| 15 | `links_in_tags` | int64 | [-1, 0, 1] |
| 16 | `sfh` | int64 | [-1, 0, 1] |
| 17 | `submitting_to_email` | int64 | [-1, 1] |
| 18 | `abnormal_url` | int64 | [-1, 1] |
| 19 | `redirect` | int64 | [0, 1] |
| 20 | `on_mouseover` | int64 | [-1, 1] |
| 21 | `rightclick` | int64 | [-1, 1] |
| 22 | `popupwindow` | int64 | [-1, 1] |
| 23 | `iframe` | int64 | [-1, 1] |
| 24 | `age_of_domain` | int64 | [-1, 1] |
| 25 | `dnsrecord` | int64 | [-1, 1] |
| 26 | `web_traffic` | int64 | [-1, 0, 1] |
| 27 | `page_rank` | int64 | [-1, 1] |
| 28 | `google_index` | int64 | [-1, 1] |
| 29 | `links_pointing_to_page` | int64 | [-1, 0, 1] |
| 30 | `statistical_report` | int64 | [-1, 1] |
