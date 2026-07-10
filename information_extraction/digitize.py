import json
from datalab_sdk import DatalabClient, ExtractOptions

client = DatalabClient()

citizenship_schema = {
  "type": "object",
  "title": "ExtractionSchema",
  "description": "Schema for structured data extraction",
  "properties": {
    "citizenship_no": {
      "type": "string",
      "description": "Official Nepal Citizenship Certificate number printed on the document. Extract the complete number exactly as shown, preserving all digits, letters (if any), hyphens, slashes, or other separators. Do not infer or modify the format. Return an empty string if not present or unreadable."
    },
    "full_name": {
      "type": "string",
      "description": "Full legal name of the citizenship certificate holder exactly as printed on the document. Preserve spelling, spacing, and order of names."
    },
    "gender": {
      "type": "string",
      "description": "Gender or sex of the certificate holder, It is either महिला or पुरुष."
    },
    "birth_district": {
      "type": "string",
      "description": "District of birth of the certificate holder."
    },
    "birth_municipality": {
      "type": "string",
      "description": "Municipality, Rural Municipality, Metropolitan City, or Sub-metropolitan City of birth."
    },
    "birth_ward": {
      "type": "string",
      "description": "Ward number of the holder's place of birth exactly as printed."
    },
    "perm_district": {
      "type": "string",
      "description": "District of the holder's permanent address."
    },
    "perm_municipality": {
      "type": "string",
      "description": "Municipality, Rural Municipality, Metropolitan City, or Sub-metropolitan City of the holder's permanent address."
    },
    "perm_ward": {
      "type": "string",
      "description": "Ward number of the holder's permanent address exactly as printed."
    },
    "dob_year": {
      "type": "string",
      "description": "Year component of the holder's date of birth exactly as printed."
    },
    "dob_month": {
      "type": "string",
      "description": "Month component of the holder's date of birth exactly as printed."
    },
    "dob_day": {
      "type": "string",
      "description": "Day component of the holder's date of birth exactly as printed."
    },
    "father_name": {
      "type": "string",
      "description": "Full name of the holder's father exactly as printed"
    },
    "father_citizenship_no": {
      "type": "string",
      "description": "Citizenship certificate number of the holder's father exactly as printed."
    },
    "father_address": {
      "type": "string",
      "description": "Citizenship certificate number of the holder's father exactly as printed."
    },
    "father_na_ki": {
      "type": "string",
      "description": "Relationship (Nata/Kisim) associated with the father exactly as printed."
    },
    "mother_name": {
      "type": "string",
      "description": "Full name of the holder's mother exactly as printed."
    },
    "mother_citizenship_no": {
      "type": "string",
      "description": "Citizenship certificate number of the holder's mother exactly as printed."
    },
    "mother_address": {
      "type": "string",
      "description": "Address of the holder's spouse exactly as printed."
    },
    "mother_na_ki": {
      "type": "string",
      "description": "Relationship (Nata/Kisim) associated with the mother exactly as printed."
    },
    "spouse_name": {
      "type": "string",
      "description": "Full name of the holder's spouse exactly as printed. Return an empty string if absent."
    },
    "spouse_citizenship_no": {
      "type": "string",
      "description": "Citizenship certificate number of the holder's spouse exactly as printed. Return an empty string if absent."
    },
    "spouse_na_ki": {
      "type": "string",
      "description": "Relationship (Nata/Kisim) associated with the spouse exactly as printed."
    },
    "district_admin_location": {
      "type": "string",
      "description": "Location of the district administration office that issued the citizenship certificate."
    }
  },
  "required": [
    "citizenship_no",
    "full_name",
    "gender",
    "birth_district",
    "birth_municipality",
    "birth_ward",
    "perm_district",
    "perm_municipality",
    "perm_ward",
    "dob_year",
    "dob_month",
    "dob_day",
    "father_name",
    "father_citizenship_no",
    "father_address",
    "father_na_ki",
    "mother_name",
    "mother_citizenship_no",
    "mother_address",
    "mother_na_ki",
    "spouse_name",
    "spouse_citizenship_no",
    "spouse_na_ki",
    "district_admin_location"
  ]
}

options = ExtractOptions( page_schema=json.dumps(citizenship_schema), mode="balanced")
result = client.extract("./data/aditya.png", options=options)
extracted = json.loads(result.extraction_schema_json)
print(f"Full Name: {extracted.get('full_name')}")
print(f"Citizenship No: {extracted.get('citizenship_no')}")
print(f"Gender: {extracted.get('gender')}")
