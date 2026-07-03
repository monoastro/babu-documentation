pip install torch transformers pymupdf
model = AutoModel.from_pretrained(“baidu/Unlimited-OCR”, trust_remote_code=True)
model.infer_multi(tokenizer, prompt=“<image>Multi page parsing.”, image_files=pages)
