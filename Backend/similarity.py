import spacy

nlp = spacy.load("en_core_web_lg")

def filter_unique_sentences(text1, text2, threshold=0.85, return_score=False, return_combined=False):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    sents1 = list(doc1.sents)
    sents2 = list(doc2.sents)

    unique_sents2 = []
    common_sentences = []
    total = len(sents2)
    matched = 0

    for s2 in sents2:
        is_similar = any(s2.similarity(s1) >= threshold for s1 in sents1)
        if not is_similar:
            unique_sents2.append(s2.text.strip())
        else:
            matched += 1
            common_sentences.append(s2.text.strip())

    similarity_percent = (matched / total) * 100 if total else 0
    combined_text = text1.strip()
    if unique_sents2:
        combined_text += "\n\n--- Unique from PDF 2 ---\n\n" + "\n\n".join(unique_sents2)

    if return_score and return_combined:
        return common_sentences, round(similarity_percent, 2), combined_text
    elif return_score:
        return common_sentences, round(similarity_percent, 2)
    else:
        return combined_text