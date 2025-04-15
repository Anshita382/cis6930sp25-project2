import spacy

def test_ner_entities():
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Elon Musk founded SpaceX in California.")

    entities = [(ent.text, ent.label_) for ent in doc.ents]

    assert ("Elon Musk", "PERSON") in entities
    assert ("SpaceX", "ORG") in entities
    assert ("California", "GPE") in entities
