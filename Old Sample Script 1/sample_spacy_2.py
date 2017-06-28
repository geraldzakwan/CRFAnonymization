import numpy
import spacy

nlp = spacy.load('en')
apples, and_, oranges = nlp(u'apples and oranges')
print(apples.vector.shape)
# (1,)
apples.similarity(oranges)
