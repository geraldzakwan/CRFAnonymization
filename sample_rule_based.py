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

    # List all locations
    org_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "org"):
            org_index_list.append(i)

    # List all token 'I'
    i_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "I" or list_of_token[i] == "i" or list_of_token[i] == "My" or list_of_token[i] == "my"):
            i_index_list.append(i)

    # List all titik
    dot_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "."):
            dot_index_list.append(i)

    print(list_of_ner)
    print(list_of_token)
    # print(loc_index_list)
    # print(org_index_list)
    # print(i_index_list)
    # print(dot_index_list)

    loc_candidate_phrases = []

    for idx_loc in loc_index_list:
        for idx_i in i_index_list:
            if(idx_i < idx_loc):
                # Cek apakah kepotong titik antara I/My dengan lokasi
                is_cut = False
                for idx_dot in dot_index_list:
                    if(idx_dot > idx_i and idx_dot < idx_loc):
                        is_cut = True

                if(not is_cut):
                    token_list = []
                    for i in range(idx_i, idx_loc+1):
                        token_list.append(list_of_token[i])
                    loc_candidate_phrases.append(token_list)

    return loc_candidate_phrases

def identify_candidate_private_organizational_phrases(ner_prediction):
    list_of_ner = [item[1] for item in ner_prediction]
    list_of_token = [item[0] for item in ner_prediction]

    # List all locations
    org_index_list = []
    for i in range(0, len(list_of_ner)):
        if(list_of_ner[i] == "org"):
            org_index_list.append(i)

    # List all token 'I'
    i_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "I" or list_of_token[i] == "i" or list_of_token[i] == "My" or list_of_token[i] == "my"):
            i_index_list.append(i)

    # List all titik
    dot_index_list = []
    for i in range(0, len(list_of_token)):
        if(list_of_token[i] == "."):
            dot_index_list.append(i)

    org_candidate_phrases = []

    for idx_org in org_index_list:
        for idx_i in i_index_list:
            if(idx_i < idx_org):
                # Cek apakah kepotong titik antara I/My dengan lokasi
                is_cut = False
                for idx_dot in dot_index_list:
                    if(idx_dot > idx_i and idx_dot < idx_org):
                        is_cut = True

                if(not is_cut):
                    token_list = []
                    for i in range(idx_i, idx_org+1):
                        token_list.append(list_of_token[i])
                    org_candidate_phrases.append(token_list)

    return org_candidate_phrases

def check_negative_phrases(list_candidate_phrases):
    candidate_phrases_without_negative = []

    for candidate_phrases in list_candidate_phrases:
        is_negative = False
        for token in candidate_phrases:
            if(token == "no" or token == "not" or token =="never"):
                is_negative = True

        if(not is_negative):
            candidate_phrases_without_negative.append(candidate_phrases)

    return candidate_phrases_without_negative
