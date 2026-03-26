"""
Restraint Documentation QI Project
Step 1: Generate realistic dummy data matching real restraint audit columns
Author: [Your Name]
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

# ── helpers ──────────────────────────────────────────────────────────────────

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_time():
    h = random.randint(0, 23)
    m = random.choice([0, 15, 30, 45])
    return f"{h:02d}:{m:02d}"

def yes_no(prob_yes=0.75):
    """Return Yes/No with configurable compliance rate."""
    return "Yes" if random.random() < prob_yes else "No"

def yes_no_na(prob_yes=0.70, prob_na=0.10):
    r = random.random()
    if r < prob_yes:
        return "Yes"
    elif r < prob_yes + prob_na:
        return "N/A"
    return "No"

# ── reference data ────────────────────────────────────────────────────────────

ORG_UNITS    = ["3 North", "4 South", "ICU", "PCU", "ED", "5 West", "2 East"]
SETTINGS     = ["Inpatient", "ED", "ICU/Critical Care"]
GENDERS      = ["Male", "Female", "Non-binary / Other"]
STAFF_TITLES = ["RN", "LVN", "CNA", "Charge RN", "Supervisor"]
DEPARTMENTS  = ["Med/Surg", "Critical Care", "Emergency", "Psychiatry", "Telemetry"]
PHYSICIANS   = ["Dr. Patel", "Dr. Nguyen", "Dr. Williams", "Dr. Garcia", "Dr. Thompson"]
SERVICE_LINES= ["Hospitalist", "Psychiatry", "Pulmonology", "Cardiology", "Neurology"]
ENTERED_BY   = ["Smith, J", "Garcia, M", "Pham, T", "Johnson, R", "Lee, S"]

START = datetime(2024, 1, 1)
END   = datetime(2024, 12, 31)

# ── build records ─────────────────────────────────────────────────────────────

N = 150  # number of restraint episodes
records = []

for i in range(1, N + 1):
    admit_date  = random_date(START, END)
    init_date   = admit_date + timedelta(days=random.randint(0, 3))
    end_date    = init_date  + timedelta(hours=random.randint(1, 72))
    disch_date  = end_date   + timedelta(days=random.randint(0, 5))
    dob         = datetime(random.randint(1940, 2000), random.randint(1, 12), random.randint(1, 28))
    age         = (admit_date - dob).days // 365
    org_unit    = random.choice(ORG_UNITS)
    setting     = "ICU/Critical Care" if org_unit == "ICU" else (
                  "ED" if org_unit == "ED" else "Inpatient")

    records.append({
        "Unique ID":                        f"RST-{i:04d}",
        "Entered By":                       random.choice(ENTERED_BY),
        "Entry Date":                       random_date(START, END).strftime("%Y-%m-%d"),
        "Observation Date":                 init_date.strftime("%Y-%m-%d"),
        "Organization":                     "Memorial Health System",
        "Org Unit":                         org_unit,
        "Primary Setting":                  setting,
        "Patient DOB":                      dob.strftime("%Y-%m-%d"),
        "Patient Age":                      age,
        "Patient Gender":                   random.choice(GENDERS),
        "Patient Admit Date":               admit_date.strftime("%Y-%m-%d"),
        "Patient Discharge Date":           disch_date.strftime("%Y-%m-%d"),
        "Unit / Bed":                       f"{org_unit}-{random.randint(101,130)}",
        "Staff Involved":                   random.choice(ENTERED_BY),
        "Staff Title":                      random.choice(STAFF_TITLES),
        "Staff Department":                 random.choice(DEPARTMENTS),

        # ── compliance fields ─────────────────────────────────────────────────
        "Restraint Discontinuation: Was the restraint documented as discontinued?":
            yes_no(0.78),
        "If a Behavioral Emergency persists after time limits, was the patient released prior to a new order?":
            yes_no_na(0.65, 0.20),
        "Was a debriefing with patient and/or patient's LAR documented?":
            yes_no(0.60),
        "Transition Period: Was the patient behavior observed for 15 minutes after discontinuation?":
            yes_no(0.70),

        "Restraint End Date":               end_date.strftime("%Y-%m-%d"),
        "Restraint End Time":               random_time(),
        "Authorizing/Attending Provider":   random.choice(PHYSICIANS),
        "Ordering Provider":                random.choice(PHYSICIANS),
        "Was the Ordering provider a physician?":
            yes_no(0.90),

        "Restraint Order: Was the restraint ordered correctly?":
            yes_no(0.82),
        "Are all components of the Restraint order complete?":
            yes_no(0.75),
        "Was a Face-to-Face Evaluation conducted within one hour of initial Restraint implementation?":
            yes_no(0.68),
        "Are all components of the Face to Face Evaluation complete (Physician/PA/APRN)?":
            yes_no(0.72),
        "Was the correct restraint type implemented per MD order?":
            yes_no(0.88),
        "Was Q 15 minute restraint monitoring complete?":
            yes_no(0.65),
        "Was Q 1 hour restraint monitoring complete?":
            yes_no(0.71),
        "Hydration/Nutrition/Toileting/Hygiene: Was the patient provided an opportunity?":
            yes_no(0.74),
        "Is there evidence the restraint was removed at the earliest possible opportunity?":
            yes_no(0.69),
        "Restraint Plan of Care: Is there evidence of an individualized Plan of Care per shift?":
            yes_no(0.63),

        "Restraint Initiation Date":        init_date.strftime("%Y-%m-%d"),
        "Restraint Initiation Time":        random_time(),
        "Transfer In Date":                 admit_date.strftime("%Y-%m-%d") if random.random() < 0.3 else "",
        "Transfer In Time":                 random_time() if random.random() < 0.3 else "",
        "Medical Record Number":            f"MRN{random.randint(1000000, 9999999)}",
        "HAR":                              f"HAR{random.randint(100000, 999999)}",
        "Physician Service Line":           random.choice(SERVICE_LINES),

        "Were the restraints implemented by an approved member of the care team?":
            yes_no(0.92),
        "Participation: Was who participated in the restraint application documented?":
            yes_no(0.73),
        "Was the least restrictive method(s) documented at the time of restraint implementation?":
            yes_no(0.66),
        "Did the patient receive education regarding restraints (per policy 7.02)?":
            yes_no(0.58),
        "Patient/Family/LAR notification: Did the RN follow the notification process?":
            yes_no(0.71),
    })

df = pd.DataFrame(records)
df.to_excel("restraints_dummy_data.xlsx", index=False)
print(f"Created restraints_dummy_data.xlsx with {len(df)} records and {len(df.columns)} columns.")
print("\nColumn preview:")
for col in df.columns:
    print(f"  {col}")
