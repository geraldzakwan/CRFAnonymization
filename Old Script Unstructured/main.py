import main_ner_2
import nltk_ner_trainer
import access_corpus
from nltk import pos_tag, word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags

# The path to the used corpus, here I used large dataset corpus named Groningen Meaning Bank
corpus_root = 'gmb-2.2.0'
mode = '--core'

data = access_corpus.read_corpus(corpus_root, mode)

training_samples = data[:int(len(data) * 0.9)]
test_samples = data[int(len(data) * 0.9):]

print "#training samples = %s" % len(training_samples)    # training samples = 55809
print "#test samples = %s" % len(test_samples)                # test samples = 6201

chunker = nltk_ner_trainer.NamedEntityChunker(training_samples[:2000])
# text = "Cristiano Ronaldo is a decent footballer both in Real Madrid, Spain and Manchester United, United Kingdom. He is truly a masterpiece."
text = "Geraldi Dzakwan wakes up at 7 am every morning."
print chunker.parse(pos_tag(word_tokenize(text)))

score = chunker.evaluate([conlltags2tree([(w, t, iob) for (w, t), iob in iobs]) for iobs in test_samples[:500]])

# Debugging
# 0.931132334092
print score.accuracy()
