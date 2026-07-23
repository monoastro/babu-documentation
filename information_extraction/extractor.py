import json

from datalab_sdk import DatalabClient, ExtractOptions

client = DatalabClient()


def load_schema(schema_path):
    with open(schema_path, encoding="utf-8") as f:
        return json.load(f)

def extract(image_path, schema_path, mode="balanced"):
    schema = load_schema(schema_path)
    options = ExtractOptions( page_schema=json.dumps(schema), mode=mode,)
    result = client.extract( image_path, options=options,)
    extracted = json.loads(result.extraction_schema_json)
    return extracted, schema

def build_data(extracted, schema):
    return { key: extracted.get(key, "") for key in schema["required"] }
