from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')

def stem_list_of_token(ner_prediction):
    stemmed_list_of_token = []

    for token_tuple in ner_prediction:
        if(token_tuple[1] == 'O'):
            stemmed_token = stemmer.stem(token_tuple[0])
        else:
            stemmed_token = token_tuple[0]

        stemmed_list_of_token.append((stemmed_token, token_tuple[1]))

    return stemmed_list_of_token
