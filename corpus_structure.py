#Script to migrate corpus to DB

import sys
import nltk
import MySQLdb

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

if(len(sys.argv) < 2):
    sys.exit('Supply corpus index')

db = MySQLdb.connect(
                        host="localhost",   # your host, usually localhost
                        user="root",        # your username
                        passwd="",          # your password
                        db="english_corpus" # name of the data base
                    )

comma = ", "
quote = "'"
cur = db.cursor()

def remove_quote(word):
    if(word[0] == "'"):
        word = word[1:len(word)-1]
    return word

if(sys.argv[1] == '1'):
    # print(nltk.corpus.conll2002.fileids())
    # ['esp.testa', 'esp.testb', 'esp.train', 'ned.testa', 'ned.testb', 'ned.train']

    train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train'))
    test_sents = list(nltk.corpus.conll2002.iob_sents('esp.testb'))
    it = 0
    query_error_list = []

    for doc in train_sents:
        for chunk in doc:
            word = chunk[0]
            pos_tag = chunk[1]
            ner = chunk[2]

            word = remove_quote(word)
            query = "INSERT INTO ner_annotated_corpus_conll2002_esp (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ")";
            try:
                cur.execute(query)
                db.commit()
            except:
                query_error_list.append(query)
                db.rollback()

            it = it + 1
            print(it)


    print('--------------')
    print('--------------')
    print('--------------')
    for query_error in query_error_list:
        print(query_error)

    print('Cannot be printed to ext file')
    print('--------------')
    print('--------------')
    print('--------------')
    thefile = open('query_error_list_conll2002_esp.txt', 'w')
    for item in query_error_list:
        try:
            thefile.write("%s\n" % item)
        except:
            print(item)

    db.close()

elif(sys.argv[1] == '2'):
    train_sents = list(nltk.corpus.conll2002.iob_sents('ned.train'))
    test_sents = list(nltk.corpus.conll2002.iob_sents('ned.testb'))
    it = 0
    query_error_list = []

    for doc in train_sents:
        for chunk in doc:
            word = chunk[0]
            pos_tag = chunk[1]
            ner = chunk[2]

            word = remove_quote(word)
            # query = "INSERT INTO ner_annotated_corpus_conll2002_ned (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ")";
            query = "INSERT INTO ner_annotated_corpus_conll2002_ned_2 (word, pos_tag, named_entity) VALUES (" + quote + word + quote + comma + quote + pos_tag + quote + comma + quote + ner + quote + ")";
            try:
                cur.execute(query)
                db.commit()
            except:
                query_error_list.append(query)
                db.rollback()

            it = it + 1
            print(it)

    print('--------------')
    print('--------------')
    print('--------------')
    for query_error in query_error_list:
        print(query_error)

    print('Cannot be printed to ext file')
    print('--------------')
    print('--------------')
    print('--------------')
    thefile = open('query_error_list_conll2002_ned.txt', 'w')
    for item in query_error_list:
        try:
            thefile.write("%s\n" % item)
        except:
            print(item)

    db.close()

elif(sys.argv[1] == '3'):
    docs = nltk.corpus.ieer.parsed_docs('APW_19980314')
    for items in docs[0].text:
        print(items)
else:
    print('Not defined')
