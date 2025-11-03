import re

# ============================================================
# SECTION 1 — PHONE NUMBERS
# ============================================================

print("\n=== SECTION 1: phone.txt ===")

with open("phone.txt") as f:
    string = f.read()

# ----------------------------
# Q1: Persons whose phone number starts with an odd digit
# ----------------------------
result1 = re.findall(r"\b[A-Z][a-z]+\s[A-Z][a-z]+\s+\(\d{3}\)\s+[13579]\d{2}-\d{4}", string)
print("\nQ1 - Full names (phone starts with odd digit):")
print(result1)

# ----------------------------
# Q2: First names only where area code < 300
# ----------------------------
result2 = re.findall(r"\b([A-Z][a-z]+)\s[A-Z][a-z]+\s+\((0\d{2}|1\d{2}|2\d{2})\)", string)
first_names_q2 = [r[0] for r in result2]
print("\nQ2 - First names (area code < 300):")
print(first_names_q2)

# ----------------------------
# Q3: First names where last name ends in vowel, number ends in 0/7/9
# ----------------------------
result3 = re.findall(r"\b([A-Z][a-z]+)\s[A-Z][a-z]*[aeiouAEIOU]\s+\(\d{3}\)\s+\d{3}-\d{3}[079]", string)
print("\nQ3 - First names (last name ends in vowel, phone ends 0/7/9):")
print(result3)


# ============================================================
# SECTION 2 — LOG ENTRIES
# ============================================================

print("\n=== SECTION 2: logs.txt ===")

with open("logs.txt") as f:
    log_data = f.read()

# ----------------------------
# Q1: Sources of log entries after 12 PM and before 4 PM
# ----------------------------
result4 = re.findall(r"\d+/\d+/\d+\s+(12|1|2|3):\d{2}:\d{2}\s+PM\s+([\w\-]+)", log_data)
sources_q1 = [r[1] for r in result4]
print("\nQ1 - Sources (time between 12 PM and 4 PM):")
print(sources_q1)

# ----------------------------
# Q2: Dates of entries where Source is TPM
# ----------------------------
result5 = re.findall(r"\b(\d+/\d+/\d+)\s+\d{1,2}:\d{2}:\d{2}\s+[AP]M\s+TPM", log_data)
print("\nQ2 - Dates (Source is TPM):")
print(result5)

# ----------------------------
# Q3: Date & Time of entries between Jan 24–27, 2020 from 8:00–8:59 AM
# ----------------------------
result6 = re.findall(r"\b(1/(2[4-7])/2020\s+8:\d{2}:\d{2}\s+AM)", log_data)
print("\nQ3 - Date & Time (Jan 24–27, 8:00–8:59 AM):")
print(result6)
