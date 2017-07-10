import re, collections
import sys

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

NWORDS = train(words(file('big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or    known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

def input_spell_correction(tokenized_input, iob_prediction):
    corrected_tokenized_input = []
    i = 0

    for token in tokenized_input:
        if("B-" not in iob_prediction[i] and "I-" not in iob_prediction[i]):
            new_token = correct(token)
        else:
            new_token = token
            
        corrected_tokenized_input.append(new_token)
        i = i + 1

    return corrected_tokenized_input

if __name__ == '__main__':
    NWORDS = train(words(file('big.txt').read()))
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    print(correct(sys.argv[1]))
