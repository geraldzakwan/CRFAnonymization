# import matplotlib.pyplot as plt
# plt.style.use('ggplot')

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

import fetch_user_profile
import google_search
import access_gmb_corpus
import feature_extraction

# train_sents = access_gmb_corpus.read_corpus_ner('gmb-2.2.0', '--core')
# test_sents = access_gmb_corpus.read_corpus_ner('gmb-2.2.0', '--core')

# X_train = [feature_extraction.sent2features(s) for s in train_sents]
# y_train = [feature_extraction.sent2labels(s) for s in train_sents]

# X_test = [feature_extraction.sent2features(s) for s in test_sents]
# y_test = [feature_extraction.sent2labels(s) for s in test_sents]

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

text_input = sys.argv[2]
tokenized_input = nltk.word_tokenize(text_input)
pos_tagged_input = nltk.pos_tag(tokenized_input)
# print(pos_tagged_input)
featured_input = feature_extraction.sent2features(pos_tagged_input)
# print(featured_input)

iob_prediction = crf.predict_single(featured_input)
# print(tokenized_input)
# print(iob_prediction)

# Kasi kasus disini, kalo dia location dibandingin ama attribut mana aja di user profil, dkk
user_dict = fetch_user_profile.get_data(sys.argv[3])
predicted_sentence_cooccurence = []

# Sebelum ini harusnya preprocessing dulu, digabungin semua yang B sama I
# List of tuple (string, ner)
ner_prediction = []
curr_items = ""
i = 0
while (i<len(iob_prediction)):
    if("B" in iob_prediction[i]):
        ner_tag = iob_prediction[i][2:]
        curr_items = tokenized_input[i]
        i = i + 1
        while("I" in iob_prediction[i]):
            curr_items = curr_items + " " + tokenized_input[i]
            i = i + 1
        ner_prediction.append((curr_items, ner_tag))
        i = i - 1
    else:
        curr_items = tokenized_input[i]
        ner_tag = iob_prediction[i]
        ner_prediction.append((curr_items, ner_tag))
    i = i + 1

for tup in ner_prediction:
    print(tup)

# i = 0
# for ner_tag in iob_prediction:
#     co_occurence = 0
#     if ("per" in ner_tag):
#         # Compare with full name
#         co_occurence = google_search.co_occurence(user_dict['full_name'], tokenized_input[i])
#     elif ("org" in ner_tag):
#         # Compare with education, work
#         co_occurence_1 = google_search.co_occurence(user_dict['education'], tokenized_input[i])
#         co_occurence_2 = google_search.co_occurence(user_dict['work'], tokenized_input[i])
#         if (co_occurence_1 > co_occurence_2):
#             co_occurence = co_occurence_1
#         else:
#             co_occurence = co_occurence_2
#     elif ("geo" in ner_tag):
#         # Compare with hometown_city, current_city,
#         co_occurence_1 = google_search.co_occurence(user_dict['education'], tokenized_input[i])
#         co_occurence_2 = google_search.co_occurence(user_dict['work'], tokenized_input[i])
#         if (co_occurence_1 > co_occurence_2):
#             co_occurence = co_occurence_1
#         else:
#             co_occurence = co_occurence_2
#
#     predicted_sentence_cooccurence.append(co_occurence)
#
#     i = i + 1
#
# print(predicted_sentence_cooccurence)

# Ambil smua yang ke tagged_named_entity
# Bandingin sama yang sama (person dgn person) dah trus baru itung co-occurence terbesarnya

# Buat yang alphanya di bawah threshold (co-occurencenya kecil), di cek lagi sama rule based approach
