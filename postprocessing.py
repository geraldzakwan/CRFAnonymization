def restructure_sentence(ret_tokenize):
    ret_sentence = ""

    for token in ret_tokenize:
        ret_sentence = ret_sentence + token + " "

    return ret_sentence
