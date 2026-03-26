"""
Restraint Documentation QI Project
Step 2: Compliance analysis, aggregation, and visualization
Author: [Your Name]

Run this AFTER 01_create_dummy_data.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── 1. Load data ──────────────────────────────────────────────────────────────

df = pd.read_excel("restraints_dummy_data.xlsx")
print(f"Loaded {len(df)} restraint episodes\n")

# ── 2. Define compliance columns ──────────────────────────────────────────────

COMPLIANCE_COLS = {
    "Restraint discontinued":           "Restraint Discontinuation: Was the restraint documented as discontinued?",
    "Released before new order":        "If a Behavioral Emergency persists after time limits, was the patient released prior to a new order?",
    "Debriefing documented":            "Was a debriefing with patient and/or patient's LAR documented?",
    "15-min observation post-restraint":"Transition Period: Was the patient behavior observed for 15 minutes after discontinuation?",
    "Ordering MD is physician":         "Was the Ordering provider a physician?",
    "Restraint ordered correctly":      "Restraint Order: Was the restraint ordered correctly?",
    "Order components complete":        "Are all components of the Restraint order complete?",
    "Face-to-Face within 1 hour":       "Was a Face-to-Face Evaluation conducted within one hour of initial Restraint implementation?",
    "F2F components complete":          "Are all components of the Face to Face Evaluation complete (Physician/PA/APRN)?",
    "Correct restraint type":           "Was the correct restraint type implemented per MD order?",
    "Q15 monitoring complete":          "Was Q 15 minute restraint monitoring complete?",
    "Q1hr monitoring complete":         "Was Q 1 hour restraint monitoring complete?",
    "Hygiene/hydration met":            "Hydration/Nutrition/Toileting/Hygiene: Was the patient provided an opportunity?",
    "Removed at earliest opportunity":  "Is there evidence the restraint was removed at the earliest possible opportunity?",
    "Plan of Care per shift":           "Restraint Plan of Care: Is there evidence of an individualized Plan of Care per shift?",
    "Approved team member":             "Were the restraints implemented by an approved member of the care team?",
    "Participation documented":         "Participation: Was who participated in the restraint application documented?",
    "Least restrictive documented":     "Was the least restrictive method(s) documented at the time of restraint implementation?",
    "Patient education documented":     "Did the patient receive education regarding restraints (per policy 7.02)?",
    "Family/LAR notification":          "Patient/Family/LAR notification: Did the RN follow the notification process?",
}

# ── 3. Calculate overall compliance rates ─────────────────────────────────────

print("=" * 60)
print("OVERALL COMPLIANCE RATES")
print("=" * 60)

compliance_summary = {}
for short_name, col in COMPLIANCE_COLS.items():
    total    = len(df[df[col].isin(["Yes", "No"])])
    yes_count= (df[col] == "Yes").sum()
    rate     = round((yes_count / total * 100), 1) if total > 0 else 0
    compliance_summary[short_name] = rate
    status = "OK " if rate >= 90 else ("WARN" if rate >= 75 else "FAIL")
    print(f"  [{status}] {short_name:<35} {rate:>5.1f}%  ({yes_count}/{total})")

# ── 4. Compliance by org unit ─────────────────────────────────────────────────

print("\n" + "=" * 60)
print("COMPLIANCE BY ORG UNIT (key metrics)")
print("=" * 60)

key_metrics = [
    "Face-to-Face within 1 hour",
    "Q15 monitoring complete",
    "Debriefing documented",
    "Patient education documented",
    "Family/LAR notification",
]

unit_summary = {}
for short_name in key_metrics:
    col = COMPLIANCE_COLS[short_name]
    filtered = df[df[col].isin(["Yes", "No"])]
    rates = filtered.groupby("Org Unit").apply(
        lambda x: round((x[col] == "Yes").sum() / len(x) * 100, 1)
    )
    unit_summary[short_name] = rates

unit_df = pd.DataFrame(unit_summary)
print(unit_df.to_string())

# ── 5. Volume by unit and service line ───────────────────────────────────────

print("\n" + "=" * 60)
print("RESTRAINT EPISODE VOLUME")
print("=" * 60)
print("\nBy Org Unit:")
print(df["Org Unit"].value_counts().to_string())
print("\nBy Physician Service Line:")
print(df["Physician Service Line"].value_counts().to_string())

# ── 6. Visualizations ────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Restraint Documentation Quality Improvement Dashboard",
             fontsize=16, fontweight="bold", y=0.98)

# -- Chart 1: Overall compliance rates (horizontal bar) ----------------------
ax1 = axes[0, 0]
names  = list(compliance_summary.keys())
rates  = list(compliance_summary.values())
colors = ["#2ecc71" if r >= 90 else ("#f39c12" if r >= 75 else "#e74c3c") for r in rates]

sorted_pairs = sorted(zip(rates, names, colors))
rates_s, names_s, colors_s = zip(*sorted_pairs)

bars = ax1.barh(names_s, rates_s, color=colors_s, edgecolor="white", height=0.7)
ax1.axvline(x=90, color="black", linestyle="--", linewidth=1, alpha=0.5, label="90% target")
ax1.set_xlim(0, 110)
ax1.set_xlabel("Compliance Rate (%)")
ax1.set_title("Overall Compliance by Metric", fontweight="bold")

for bar, rate in zip(bars, rates_s):
    ax1.text(rate + 0.5, bar.get_y() + bar.get_height()/2,
             f"{rate}%", va="center", fontsize=8)

patches = [
    mpatches.Patch(color="#2ecc71", label="≥ 90% (target met)"),
    mpatches.Patch(color="#f39c12", label="75–89% (monitor)"),
    mpatches.Patch(color="#e74c3c", label="< 75% (action needed)"),
]
ax1.legend(handles=patches, fontsize=7, loc="lower right")
ax1.tick_params(axis="y", labelsize=7)

# -- Chart 2: Key metrics by org unit (heatmap) ------------------------------
ax2 = axes[0, 1]
heatmap_data = unit_df[key_metrics].T
im = ax2.imshow(heatmap_data.values, cmap="RdYlGn", vmin=0, vmax=100, aspect="auto")
ax2.set_xticks(range(len(heatmap_data.columns)))
ax2.set_xticklabels(heatmap_data.columns, rotation=45, ha="right", fontsize=8)
ax2.set_yticks(range(len(heatmap_data.index)))
ax2.set_yticklabels(heatmap_data.index, fontsize=7)
ax2.set_title("Key Metrics by Org Unit (%)", fontweight="bold")
plt.colorbar(im, ax=ax2, shrink=0.8)

for i in range(len(heatmap_data.index)):
    for j in range(len(heatmap_data.columns)):
        val = heatmap_data.values[i, j]
        ax2.text(j, i, f"{val:.0f}%", ha="center", va="center",
                 fontsize=8, color="black")

# -- Chart 3: Volume by org unit (bar) ---------------------------------------
ax3 = axes[1, 0]
vol = df["Org Unit"].value_counts()
ax3.bar(vol.index, vol.values, color="#3498db", edgecolor="white")
ax3.set_title("Restraint Episodes by Org Unit", fontweight="bold")
ax3.set_xlabel("Org Unit")
ax3.set_ylabel("Number of Episodes")
for i, (unit, count) in enumerate(vol.items()):
    ax3.text(i, count + 0.3, str(count), ha="center", fontsize=9)

# -- Chart 4: Bottom 5 compliance metrics (opportunity chart) ----------------
ax4 = axes[1, 1]
bottom5 = sorted(compliance_summary.items(), key=lambda x: x[1])[:5]
labels4, values4 = zip(*bottom5)
gap = [90 - v for v in values4]

ax4.barh(labels4, values4, color="#e74c3c", label="Current rate", height=0.5)
ax4.barh(labels4, gap, left=values4, color="#fadbd8", label="Gap to 90% target", height=0.5)
ax4.axvline(x=90, color="black", linestyle="--", linewidth=1)
ax4.set_xlim(0, 100)
ax4.set_xlabel("Compliance Rate (%)")
ax4.set_title("Top 5 Opportunities to Improve", fontweight="bold")
ax4.legend(fontsize=8)
ax4.tick_params(axis="y", labelsize=8)
for i, (val, lbl) in enumerate(zip(values4, labels4)):
    ax4.text(val - 1, i, f"{val}%", va="center", ha="right",
             color="white", fontsize=8, fontweight="bold")

plt.tight_layout()
plt.savefig("restraint_qi_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nDashboard saved to: restraint_qi_dashboard.png")

# ── 7. Export summary to Excel ───────────────────────────────────────────────

summary_df = pd.DataFrame({
    "Metric": list(compliance_summary.keys()),
    "Compliance Rate (%)": list(compliance_summary.values()),
    "Status": ["Met (≥90%)" if v >= 90 else ("Monitor (75-89%)" if v >= 75 else "Action Needed (<75%)")
               for v in compliance_summary.values()]
}).sort_values("Compliance Rate (%)").reset_index(drop=True)

summary_df.to_excel("restraint_compliance_summary.xlsx", index=False)
print("Summary exported to: restraint_compliance_summary.xlsx")
print("\nAnalysis complete.")
