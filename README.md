# Restraint Documentation QI — Python Analytics Project

A clinical quality improvement tool built in Python to analyze restraint documentation compliance across inpatient units. This project was developed to demonstrate data analytics skills applied to a real healthcare compliance use case.

---

## Background

Hospital restraint documentation is a high-stakes compliance area governed by CMS Conditions of Participation and The Joint Commission standards. Incomplete documentation creates regulatory risk and, more importantly, patient safety gaps. This project automates the analysis of restraint audit data — work that is typically done manually in Excel.

---

## What This Project Does

- Generates a realistic 150-record restraint audit dataset matching real EHR export columns
- Calculates compliance rates for 20 documentation metrics
- Aggregates compliance by org unit and physician service line
- Produces a four-panel QI dashboard (PNG)
- Exports a prioritized opportunity summary to Excel

---

## Files

| File | Purpose |
|---|---|
| `01_create_dummy_data.py` | Generates `restraints_dummy_data.xlsx` with 150 realistic records |
| `02_restraint_analysis.py` | Runs all analysis and produces the dashboard and summary |
| `restraints_dummy_data.xlsx` | Auto-generated dummy dataset (do not commit real data) |
| `restraint_qi_dashboard.png` | Output: four-panel compliance dashboard |
| `restraint_compliance_summary.xlsx` | Output: prioritized compliance table |

---

## How to Run

1. Install dependencies:
```
pip install pandas matplotlib openpyxl
```

2. Generate dummy data:
```
python 01_create_dummy_data.py
```

3. Run the analysis:
```
python 02_restraint_analysis.py
```

---

## Compliance Metrics Analyzed

The tool evaluates 20 documentation elements including:

- Restraint order completeness
- Face-to-Face evaluation within 1 hour of initiation
- Q15-minute and Q1-hour monitoring documentation
- Debriefing with patient/LAR
- Patient education (per policy 7.02)
- Family/LAR notification
- Least restrictive method documentation
- Plan of Care per shift
- Restraint discontinued and documented

Each metric is flagged as:
- **Met** — ≥ 90% compliance (green)
- **Monitor** — 75–89% compliance (yellow)
- **Action Needed** — < 75% compliance (red)

---

## Skills Demonstrated

- Python (pandas, matplotlib)
- Healthcare compliance domain knowledge
- Clinical data aggregation and groupby analysis
- QI dashboard design
- Translating regulatory requirements into measurable metrics

---

## Author

Clinical Informatics Analyst | Master of Biomedical Informatics  
[Add your LinkedIn and contact info here]

---

## Disclaimer

All patient data in this repository is entirely synthetic. No real patient information was used.
