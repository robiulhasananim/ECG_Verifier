import json
from datetime import date

# === (1) আপনার JSON ফাইলের পথ দিন ===
json_path = "data/ecg_data.json"

# === (2) যে date যোগ করতে চান ===
# today = date.today().isoformat()   # যদি আজকের date দিয়ে চান
fixed_date = "-25"
fixed_label = "normal ECG"

# JSON লোড
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# সব রেকর্ডে date যোগ করা
for key in data:
    data[key]["date"] = fixed_date
    data[key]["ECG_Label"] = fixed_label

# নতুন ফাইল হিসেবে সেভ
output_path = "ecg_data_updated.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✔ Done! Updated file saved as:", output_path)
