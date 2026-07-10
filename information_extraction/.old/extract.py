import json
import ast

with open("output.json", "r", encoding="utf-8") as file:
    raw_content = file.read().strip()

try:
    data = json.loads(raw_content)
except json.JSONDecodeError:
    data = ast.literal_eval(raw_content)

information = data.get("extraction_schema_json", {})

name = information.get("full_name")
citizenship_no = information.get("citizenship_no")
gender = information.get("gender")

print(f"Full Name: {name}")
print(f"Citizenship No: {citizenship_no}")
print(f"Gender: {gender}")

