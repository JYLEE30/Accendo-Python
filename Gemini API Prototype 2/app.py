from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            pdf_text = extract_text_from_pdf(file)
            return pdf_text
    return 'No file uploaded or file format not supported.'

def extract_text_from_pdf(uploaded_file):
    text = ""
    reader = PyPDF2.PdfFileReader(uploaded_file)
    for page_num in range(reader.numPages):
        text += reader.getPage(page_num).extractText()
    return text

if __name__ == '__main__':
    app.run(debug=True)