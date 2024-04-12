from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__)

# Define the directory where PDF files are stored
PDF_DIR = "./pdfs"

@app.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    # Serve PDF files from the specified directory
    return send_from_directory(PDF_DIR, filename)

@app.route('/view/<path:filename>')
def view_pdf(filename):
    # Render the HTML template with PDF viewer
    return render_template('pdf_viewer.html', pdf_url=f'/pdfs/{filename}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port="8502")
