import json
import re
import pandas as pd

# ============ FUNCTION TO CLEAN VALUES ============
def clean_value(value):
    if value is None:
        return value

    value = str(value).strip()

    # 1) Extract pure number values (2 Years -> 2, 72 ms -> 72, 102 bpm -> 102)
    num_match = re.fullmatch(r"(\d+)\s*(Years|Year|ms|bpm)?", value, re.IGNORECASE)
    if num_match:
        return num_match.group(1)

    # 2) QT/QTcBaz format: "326/424 ms" OR "444 / 396 ms"
    qt_match = re.fullmatch(r"(\d+)\s*/\s*(\d+)\s*ms", value, re.IGNORECASE)
    if qt_match:
        return f"{qt_match.group(1)}/{qt_match.group(2)}"

    # 3) P/QRS/T format: "47 / -14 / 19 degrees"
    pqt_match = re.fullmatch(r"(-?\d+)\s*/\s*(-?\d+)\s*/\s*(-?\d+)\s*degrees", value, re.IGNORECASE)
    if pqt_match:
        return f"{pqt_match.group(1)}/{pqt_match.group(2)}/{pqt_match.group(3)}"

    # 4) ECG label capitalize
    if value.lower() == "normal ecg":
        return "Normal ECG"
    if value.lower() == "abnormal ecg":
        return "Abnormal ECG"

    # 5) If nothing matches, return original
    return value


# ============ LOAD JSON FILE ============
json_file = "final_ecg_data.json"        # your JSON path
output_excel = "output.xlsx"   # output

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for filename, info in data.items():
    row = {"filename": filename}
    for key, value in info.items():
        row[key] = clean_value(value)
    rows.append(row)

df = pd.DataFrame(rows)
df.to_excel(output_excel, index=False)

print("Excel created:", output_excel)
