import matplotlib.pyplot as plt
plt.style.use('ggplot')

from itertools import chain

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics

import cPickle
import os
import sys
import collections

def to_conll_iob(annotated_sentence):
    """
    `annotated_sentence` = list of triplets [(w1, t1, iob1), ...]
    Transform a pseudo-IOB notation: O, PERSON, PERSON, O, O, LOCATION, O
    to proper IOB notation: O, B-PERSON, I-PERSON, O, O, B-LOCATION, O
    """
    proper_iob_tokens = []
    for idx, annotated_token in enumerate(annotated_sentence):
        tag, word, ner = annotated_token

        if ner != 'O':
            if idx == 0:
                ner = "B-" + ner
            elif annotated_sentence[idx - 1][2] == ner:
                ner = "I-" + ner
            else:
                ner = "B-" + ner
        proper_iob_tokens.append((tag, word, ner))
    return proper_iob_tokens

def read_corpus_ner(corpus_root, mode):
    ret_list = []

    # Create collections.Counter structure data
    # It is basically to count occurence of the words
    ner_count = collections.Counter()
    postag_count = collections.Counter()
    word_count = collections.Counter()

    # Debugging
    # print(type(ner_tags))

    # Debugging
    # Simply to count how many files are processed
    count_tag_file = 0
    # Simply to determine the total file size
    sum_file_size = 0
    # Exit point
    exit = False
    # Iterator
    it = 0

    #Iterate through all the files
    for root, dirs, files in os.walk(corpus_root):
        # if (exit):
        #     break;
        for filename in files:
            # if (exit):
            #     break;
            # Only process tag file
            if filename.endswith("en.tags"):
                count_tag_file = count_tag_file + 1
                sum_file_size = sum_file_size + os.path.getsize(os.path.join(root, filename))

                # Open the full path
                with open(os.path.join(root, filename), 'rb') as file_handle:
                    # Decode file content
                    file_content = file_handle.read().decode('utf-8').strip()

                    # Split sentences, sentences are separated with two newline characters
                    annotated_sentences = file_content.split('\n\n')

                    # Iterate through sentences
                    for annotated_sentence in annotated_sentences:

                        # Split words, words are separated with a newline character
                        annotated_tokens = [seq for seq in annotated_sentence.split('\n') if seq]

                        standard_form_tokens = []

                        for idx, annotated_token in enumerate(annotated_tokens):
                            # Split annotations, annotations are separated with a tab character
                            annotations = annotated_token.split('\t')

                            # The 1st annotation is the word itself, the 2nd is pos_tag, and the 3rd is it's named entity
                            word, pos_tag, ner = annotations[0], annotations[1], annotations[3]

                            if (mode == '--all'):
                                # Get all category including subcategory
                                ner_count[ner] += 1
                            elif (mode == '--core'):
                                # Get only the primary category
                                if ner != 'O':
                                    ner = ner.split('-')[0]

                                # Make it NLTK compatible
                                # Doesn't need it anymore since we're going to use scikit learn
                                # if pos_tag in ('LQU', 'RQU'):
                                #     pos_tag = "``"

                                standard_form_tokens.append((word, pos_tag, ner))

                                ner_count[ner] += 1
                            else:
                                sys.exit('Wrong arguments supplied.')

                            postag_count[pos_tag] += 1
                            word_count[word] += 1

                        conll_tokens = to_conll_iob(standard_form_tokens)

                        # This is to return list
                        # Make it NLTK Classifier compatible - [(w1, t1, iob1), ...] to [((w1, t1), iob1), ...]
                        # Because the classfier expects a tuple as input, first item input, second the class
                        # tuple_to_be_inserted = [((w, t), iob) for w, t, iob in conll_tokens]
                        # ret_list.append(tuple_to_be_inserted)
                        ret_list.append(conll_tokens)

                        # This is to use generator
                        # print('-------------------')
                        # for item in conlltags2tree(conll_tokens):
                        #     print(item)
                        # print('-------------------')
                        # print(conlltags2tree(conll_tokens))
                        # yield conlltags2tree(conll_tokens)

                        # Debugging
                        it = it + 1
                        print(it)

    # This is to return list
    return ret_list

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, postag, label in sent]

def sent2tokens(sent):
    return [token for token, postag, label in sent]

# print(nltk.corpus.conll2002.fileids())
# ['esp.testa', 'esp.testb', 'esp.train', 'ned.testa', 'ned.testb', 'ned.train']

# train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train'))
# test_sents = list(nltk.corpus.conll2002.iob_sents('esp.testb'))
# train_sents = read_corpus_ner('gmb-2.2.0', '--core')
# test_sents = read_corpus_ner('gmb-2.2.0', '--core')

# print('Sample sentences:')
# print(test_sents[0])
# print('-----------------')
# print(test_sents[1])
# print('-----------------')

# print('Feature extractions:')
# print(sent2features(train_sents[0])[0])
# print('-----------------')
# print('-----------------')
# print()
# print()

# X_train = [sent2features(s) for s in train_sents]
# y_train = [sent2labels(s) for s in train_sents]
#
# X_test = [sent2features(s) for s in test_sents]
# y_test = [sent2labels(s) for s in test_sents]

load = True

if(not load):
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=1000,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    # Save model
    with open(sys.argv[1], 'wb') as fid:
        cPickle.dump(crf, fid)
else:
    with open(sys.argv[1], 'rb') as fid:
        crf = cPickle.load(fid)

# labels = list(crf.classes_)
# labels.remove('O')
#
# y_pred = crf.predict(X_test)

# print('Accuration:')
# print(metrics.flat_f1_score(y_test, y_pred, average='weighted', labels=labels))
# print('-----------------')
# print('-----------------')
# print()
# print()
#
# print('Confusion matrix:')
# # group B and I results
# sorted_labels = sorted(
#     labels,
#     key=lambda name: (name[1:], name[0])
# )
# print(metrics.flat_classification_report(
#     y_test, y_pred, labels=sorted_labels, digits=3
# ))
# print('-----------------')
# print('-----------------')
# print()
# print()

# print(test_sents[0])
# for items in test_sents[0]:
#     print items[2],
# print ''
# print('-----------------')
# print(y_pred[0])

text_input = sys.argv[2]
tokenized_input = nltk.word_tokenize(text_input)
pos_tagged_input = nltk.pos_tag(tokenized_input)
# print(pos_tagged_input)
featured_input = sent2features(pos_tagged_input)
# print(featured_input)

single_sentence_prediction = crf.predict_single(featured_input)
print(single_sentence_prediction)

# Kasi kasus disini, kalo dia location dibandingin ama apa, dkk
