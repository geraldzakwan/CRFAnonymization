import spacy
nlp = spacy.load('en')
doc = nlp(u'John Smith is playing football in the University of Tokyo at 4 pm at Gifu, Japan')
for ent in doc.ents:
    print(ent.label_, ent.text)
    # GPE London
    # GPE United Kingdom
