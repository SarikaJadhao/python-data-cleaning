# =====================================================
# Python Script: Extreme Messy Data Cleaner
# =====================================================

import pandas as pd
import re

# -----------------------------------------------------
# 1. Read CSV safely
# -----------------------------------------------------
df = pd.read_csv("input_data.csv", dtype=str)

# -----------------------------------------------------
# 2. Remove duplicate rows
# -----------------------------------------------------
df = df.drop_duplicates()

# -----------------------------------------------------
# 3. Clean AGE column
# - Convert text to number
# - Remove negative / impossible ages
# - Fill missing with average
# -----------------------------------------------------
df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df.loc[(df["Age"] < 18) | (df["Age"] > 65), "Age"] = None
df["Age"] = df["Age"].fillna(df["Age"].mean()).round()

# -----------------------------------------------------
# 4. Clean SALARY column
# - Convert text like "not known"
# - Remove unrealistic salaries
# - Fill missing with median
# -----------------------------------------------------
df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
df.loc[(df["Salary"] < 10000) | (df["Salary"] > 500000), "Salary"] = None
df["Salary"] = df["Salary"].fillna(df["Salary"].median())

# -----------------------------------------------------
# 5. Clean TEXT columns
# -----------------------------------------------------
text_cols = ["Name", "Gender", "Department", "City"]

for col in text_cols:
    df[col] = df[col].fillna("Unknown")
    df[col] = df[col].str.strip()
    df[col] = df[col].replace("", "Unknown")

# -----------------------------------------------------
# 6. Normalize Gender values
# -----------------------------------------------------
df["Gender"] = df["Gender"].str.upper()
df["Gender"] = df["Gender"].replace(
    {"MALE": "M", "FEMALE": "F", "UNKNOWN": "Unknown"}
)

# -----------------------------------------------------
# 7. Clean JoiningDate (ALL formats)
# -----------------------------------------------------
df["JoiningDate"] = pd.to_datetime(
    df["JoiningDate"],
    errors="coerce",
    dayfirst=True
)

df["JoiningDate"] = df["JoiningDate"].fillna(pd.Timestamp("2000-01-01"))

# -----------------------------------------------------
# 8. Validate EMAIL
# -----------------------------------------------------
def valid_email(email):
    if pd.isna(email):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, str(email)) is not None

df["Email"] = df["Email"].apply(
    lambda x: x if valid_email(x) else "Unknown"
)

# -----------------------------------------------------
# 9. Validate PHONE numbers
# - Keep only 10-digit numbers
# -----------------------------------------------------
def clean_phone(phone):
    phone = str(phone)
    return phone if phone.isdigit() and len(phone) == 10 else "Unknown"

df["Phone"] = df["Phone"].apply(clean_phone)

# -----------------------------------------------------
# 10. Final column ordering (clean look)
# -----------------------------------------------------
final_columns = [
    "EmpID", "Name", "Age", "Gender",
    "Department", "City", "Salary",
    "JoiningDate", "Email", "Phone"
]

df = df[final_columns]

# -----------------------------------------------------
# 11. Save cleaned output
# -----------------------------------------------------
df.to_csv("cleaned_data.csv", index=False)

print("✅ Extreme messy data cleaned successfully!")
