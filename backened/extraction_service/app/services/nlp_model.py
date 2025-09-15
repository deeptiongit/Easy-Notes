import spacy

nlp = spacy.load("en_core_web_sm")

def nlp_func(text:str):

    doc = nlp(text)
    return doc.ents


