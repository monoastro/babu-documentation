import os
import subprocess
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
UPLOAD_FOLDER.mkdir(exist_ok=True)
PROJECT_ROOT = Path(__file__).parent.parent

HTML_SHELL = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Processor</title>
    <style>
        body { font-family: -apple-system, system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 2rem; background: #f5f5f5;}
        .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .form-group { margin-bottom: 1rem; }
        label { display: block; margin-bottom: 0.5rem; font-weight: bold; }
        button { background: #4a90d9; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; }
        button:hover { background: #357abd; }
        select, input[type="file"] { padding: 0.5rem; border: 1px solid #ccc; border-radius: 4px; width: 100%; max-width: 300px; }
        #output-container { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); display: none; }
        #loading { display: none; margin-top: 1rem; color: #666; font-style: italic; }
        [contenteditable]:hover { outline: 2px dashed #4a90d9; }
        [contenteditable]:focus { outline: 2px solid #4a90d9; background: #fffde7; }
    </style>
</head>
<body>
    <h1>Document Processing Pipeline</h1>
    <div class="card">
        <form id="uploadForm" enctype="multipart/form-data">
            <div class="form-group">
                <label for="doctype">Document Type</label>
                <select id="doctype" name="document_type">
                    <option value="laalpurja">Laalpurja</option>
                    <option value="citizenship">Citizenship</option>
                </select>
            </div>

            <div class="form-group">
                <label for="file">Upload Document Image</label>
                <input type="file" id="file" name="file" accept="image/png, image/jpeg" required>
            </div>

            <button type="submit">Process Document</button>
            <div id="loading">Processing... (this may take a minute)</div>
        </form>
    </div>

    <div id="output-container">
        <h2>Output (Editable)</h2>
        <div id="result-html"></div>
    </div>

    <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            const formData = new FormData(form);

            document.getElementById('loading').style.display = 'block';
            document.getElementById('output-container').style.display = 'none';
            document.querySelector('button[type="submit"]').disabled = true;

            try {
                const response = await fetch('/process', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();

                if (response.ok) {
                    document.getElementById('result-html').innerHTML = data.html;
                    document.getElementById('output-container').style.display = 'block';
                } else {
                    alert('Error: ' + data.error);
                }
            } catch (err) {
                alert('Request failed');
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.querySelector('button[type="submit"]').disabled = false;
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_SHELL)

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return jsonify(error="No file uploaded"), 400

    file = request.files['file']
    doc_type = request.form.get('document_type', 'laalpurja')

    if file.filename == '':
        return jsonify(error="No file selected"), 400

    image_path = UPLOAD_FOLDER / file.filename
    file.save(image_path)

    try:
        cmd = [
            "python", "-m", "controller.run",
            str(image_path),
            "--document-type", doc_type
        ]

        process = subprocess.run(
            cmd,
            cwd=PROJECT_ROOT,
            input="approve\\n",
            text=True,
            capture_output=True
        )

        if process.returncode != 0:
            return jsonify(error=f"Pipeline failed: {process.stderr}"), 500

        output_html = PROJECT_ROOT / "output" / f"{doc_type}.html"

        if not output_html.exists():
            return jsonify(error="Output HTML file wasn't created by pipeline"), 500

        with open(output_html, "r", encoding="utf-8") as f:
            html_content = f.read()

        return jsonify(html=html_content)

    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        if image_path.exists():
            image_path.unlink()

if __name__ == '__main__':
    print("Starting preview server on http://localhost:5000")
    app.run(debug=True, port=5000)
