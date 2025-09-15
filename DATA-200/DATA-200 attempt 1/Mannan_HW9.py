import re

f = open(r"DATA-200/phone.txt")

string = f.read()

result = re.findall(r"([A-Z][a-z]+ [A-Z][a-z]+)\s+\(([13579]\d{2})\)", string)

print(result)

result = re.findall(r"\b([A-Z][a-z]+)\b\s+[A-Z][a-z]+\s+\(\s*(?:[0-1]\d{2}|2[0-4]\d|25[0-5])\)", string)

print(result)

result = re.findall(r"\b([A-Z][a-z]+)\b\s+[A-Z][a-z]*[aeiouAEIOU]\s+\(\d{3}\)\s+\d{3}-\d{3}[079]\b", string)

print(result)

f.close()     

f = open(r"DATA-200/logs.txt")

string = f.read()

result = re.findall(r"\d+/\d+/\d+\s+(1[2-5]):\d{2}:\d{2}\s+(?:AM|PM)\s+([A-Za-z0-9\-]+)", string)

print(result)

result = re.findall(r"(\d+/\d+/\d+)\s+\d{1,2}:\d{2}:\d{2}\s+(?:AM|PM)\s+TPM", string)

print(result)

result = re.findall(r"(1/2[4-7]/2020\s+8:\d{2}:\d{2}\s+AM)", string)

print(result)