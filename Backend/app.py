# ---------------- app.py ----------------
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from extract import extract_text
from similarity import filter_unique_sentences
from pdf_creator import create_highlighted_pdf
import io
import traceback
import zipfile

app = Flask(__name__)
CORS(app, supports_credentials=True, expose_headers=["X-Similarity-Percent"])

@app.route('/upload', methods=['POST'])
def upload():
    try:
        pdf1 = request.files.get("pdf1")
        pdf2 = request.files.get("pdf2")
        threshold = float(request.form.get("threshold", 0.85))

        if not pdf1 or not pdf2:
            return jsonify({"error": "Both PDFs required"}), 400

        text1 = extract_text(pdf1.stream)
        pdf1.stream.seek(0)
        text2 = extract_text(pdf2.stream)

        common_sentences, similarity_score, combined_text = filter_unique_sentences(
            text1, text2, threshold=threshold, return_score=True, return_combined=True
        )
        
        


        pdf1_highlighted = create_highlighted_pdf(pdf1.stream, text1, common_sentences)
        pdf2_highlighted = create_highlighted_pdf(pdf2.stream, text2, common_sentences)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.writestr("pdf1_highlighted.pdf", pdf1_highlighted.getvalue())
            zip_file.writestr("pdf2_highlighted.pdf", pdf2_highlighted.getvalue())
            zip_file.writestr("combined_text.txt", combined_text)

        zip_buffer.seek(0)
        response = send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='highlighted_pdfs.zip'
        )
        response.headers["X-Similarity-Percent"] = str(similarity_score)
        return response

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
