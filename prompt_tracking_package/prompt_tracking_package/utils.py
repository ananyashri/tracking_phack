import stanza

def extract_keywords_stanza(text, nlp):
    doc = nlp(text)
    keywords = [word.text for sentence in doc.sentences for word in sentence.words if word.upos in {"NOUN", "PROPN"}]
    return list(set(keywords))

def calculate_semantic_similarity_stanza(text1, text2, nlp):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    tokens1 = {word.lemma for sentence in doc1.sentences for word in sentence.words}
    tokens2 = {word.lemma for sentence in doc2.sentences for word in sentence.words}

    common_tokens = tokens1 & tokens2
    total_tokens = tokens1 | tokens2

    return len(common_tokens) / len(total_tokens) if total_tokens else 0
