import sys
import nltk

# text_input = sys.argv[1]
# tokenized_input = nltk.word_tokenize(text_input)
# pos_tagged_input = nltk.pos_tag(tokenized_input)
#
# print(pos_tagged_input)

def identify_candidate_private_locational_phrases(ner_prediction):
    # print(ner_prediction)

    list_of_ner = [item[1] for item in ner_prediction]
    list_of_token = [item[0] for item in ner_prediction]

    # List all locations
    loc_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "geo"):
            loc_index_list.append(i)

    # List all token 'I'
    i_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "I" or list_of_token[i] == "i"):
            i_index_list.append(i)

    # List all titik
    dot_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "."):
            dot_index_list.append(i)

    print(list_of_ner)
    # print(loc_index_list)
    print(list_of_token)
    # print(i_index_list)
    # print(dot_index_list)
