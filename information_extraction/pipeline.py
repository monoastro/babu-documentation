from document_builder.registry import DOCUMENTS
from information_extraction.extractor import ( extract, build_data,)

def build_document(document_type, image_path):
    config = DOCUMENTS[document_type]
    extracted, schema = extract( image_path=image_path, schema_path=config["schema"],)
    data = build_data( extracted, schema)
    builder = config["builder"]
    return builder(data)

def digitize_document(document_type, image_path, output_path = "output.html"):
    doc = build_document( document_type, image_path,)
    doc.save(str(output_path))
