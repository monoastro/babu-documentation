from document_builder.registry import DOCUMENTS
from information_extraction.extractor import ( extract, build_data,)
from information_extraction.translator import DEFAULT_LANGUAGE, translate_data

def build_document(document_type, image_path, translate = True, target_language = DEFAULT_LANGUAGE):
    config = DOCUMENTS[document_type]
    extracted, schema = extract( image_path=image_path, schema_path=config["schema"],)
    data = build_data( extracted, schema)
    if translate:
        # A failed translation is reported, not raised: a document rendered in
        # Devanagari is more useful than no document.
        result = translate_data(data, target_language=target_language, verbose=True)
        print(f"  translation: {result.describe()}")
        data = result.data
    builder = config["builder"]
    return builder(data)

def digitize_document(document_type, image_path, output_path = "output.html", translate = True, target_language = DEFAULT_LANGUAGE):
    doc = build_document( document_type, image_path, translate=translate, target_language=target_language,)
    doc.save(str(output_path))
