from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
import tag_converter

stemmer = SnowballStemmer('english')
# stemmer = PorterStemmer()
# stemmer = LancasterStemmer()
stemmer.stem('maximum')

wordnet_lemmatizer = WordNetLemmatizer()

def stem_list_of_token(ner_prediction):
    stemmed_list_of_token = []

    for token_tuple in ner_prediction:
        if(token_tuple[1] == 'O'):
            stemmed_token = stemmer.stem(token_tuple[0])
        else:
            stemmed_token = token_tuple[0]

        stemmed_list_of_token.append((stemmed_token, token_tuple[1]))

    return stemmed_list_of_token

def lemmatize_list_of_token(ner_prediction, pos_tag_list):
    lemmatized_list_of_token = []

    i = 0
    for token_tuple in ner_prediction:
        if(token_tuple[1] == 'O'):
            tag = tag_converter.penn_to_wn(pos_tag_list[i])
            lemmatized_token = wordnet_lemmatizer.lemmatize(token_tuple[0], pos=tag)
            print(lemmatized_token)
        else:
            lemmatized_token = token_tuple[0]
        i = i + 1

        lemmatized_list_of_token.append((lemmatized_token, token_tuple[1]))

    return lemmatized_list_of_token
