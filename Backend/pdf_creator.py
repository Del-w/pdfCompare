import fitz  # PyMuPDF
import io
from difflib import SequenceMatcher

def best_fuzzy_match(sentence, text_lines):
    best_ratio = 0
    best_match = None
    for line in text_lines:
        ratio = SequenceMatcher(None, sentence, line).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_match = line
    return best_match if best_ratio > 0.8 else None  # Tune threshold here

def create_highlighted_pdf(pdf_stream, original_text, common_sentences):
    pdf_stream.seek(0)
    doc = fitz.open(stream=pdf_stream.read(), filetype="pdf")

    for page in doc:
        page_lines = page.get_text("text").splitlines()

        for sentence in common_sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 5:
                continue

            best_match = best_fuzzy_match(sentence, page_lines)
            if best_match:
                instances = page.search_for(best_match)
                for inst in instances:
                    page.add_highlight_annot(inst)

    output_stream = io.BytesIO()
    doc.save(output_stream)
    doc.close()
    output_stream.seek(0)
    return output_stream
