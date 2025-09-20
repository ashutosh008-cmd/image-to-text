from flask import Flask, render_template, request, jsonify
import easyocr
import os

app = Flask(__name__)
reader = easyocr.Reader(['en'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'files' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400

    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        return jsonify({'error': 'No files selected'}), 400

    extracted_texts = []
    for file in files:
        if file.filename != '':
            image_path = f"temp_{file.filename}"
            file.save(image_path)
            result = reader.readtext(image_path)
            extracted_text = "\n".join([detection[1] for detection in result])
            extracted_texts.append(f"--- {file.filename} ---\n{extracted_text}\n")
            os.remove(image_path)

    return jsonify({'text': "\n".join(extracted_texts)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
