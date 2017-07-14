import sys
import nltk
import sklearn
import sklearn_crfsuite
import cPickle

import fetch_user_profile
import google_search
import access_gmb_corpus
import feature_extraction
import anonymization
import postprocessing
import sentence_similarity
import sample_rule_based
import normalization
import spell_checker
import temporal_phrase_tagger
import location_generalization
import genderize

def load_or_train_crf(load, filename):
    crf = None

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
        with open(filename, 'wb') as fid:
            cPickle.dump(crf, fid)
    else:
        with open(filename, 'rb') as fid:
            crf = cPickle.load(fid)

    return crf

def do_pos_tag(text_input):
    tokenized_input = nltk.word_tokenize(text_input)

    # Spell checking disini, tapi ternyata yang named entity ikut keubah jadi jangan
    # tokenized_input = spell_checker.input_spell_correction(tokenized_input)
    # print(tokenized_input)

    pos_tagged_input = nltk.pos_tag(tokenized_input)

    # Normalized here
    stemmed_tokenized_output = normalization.stem_list_of_token_awal(pos_tagged_input)
    # print('Stemmed: ', stemmed_tokenized_output)

    normalized_tokenized_output = normalization.lemmatize_list_of_token_awal(stemmed_tokenized_output)

    # print('Lemmatized: ', normalized_tokenized_output)
    return normalized_tokenized_output

def extract_features(pos_tagged_input):
    featured_input = feature_extraction.sent2features(pos_tagged_input)
    # print(featured_input)
    return featured_input

def predict_named_entity(crf, featured_input):
    iob_prediction = crf.predict_single(featured_input)
    # print(tokenized_input)

    return iob_prediction

    # Spell checking disini aja setelah predict named entity
    # Kadang masih sering error ini
    # tokenized_input = spell_checker.input_spell_correction(tokenized_input, iob_prediction)
    # print('Spell checking')
    # print(tokenized_input)

    # Print prediction in IOB format
    # print(iob_prediction)

def combine_named_entity_chunks(pos_tagged_input, iob_prediction):
    # Sebelum ini harusnya preprocessing dulu, digabungin semua yang B sama I
    # List of tuple (string, ner)
    ner_prediction = []
    curr_items = ""
    i = 0

    while (i<len(iob_prediction)):
        if("B" in iob_prediction[i]):
            ner_tag = iob_prediction[i][2:]
            # curr_items = tokenized_input[i]
            curr_items = pos_tagged_input[i][0]
            i = i + 1
            while("I" in iob_prediction[i]):
                # curr_items = curr_items + " " + tokenized_input[i]
                curr_items = curr_items + " " + pos_tagged_input[i][0]
                i = i + 1
                # Buggy for end of sentence : if(i >= len(iob_prediction)-1):
                if(i >= len(iob_prediction)):
                    break
            tuple_list = []
            tuple_list.append(curr_items)
            tuple_list.append(ner_tag)
            ner_prediction.append(tuple_list)
            i = i - 1
        else:
            # curr_items = tokenized_input[i]
            curr_items = pos_tagged_input[i][0]
            ner_tag = iob_prediction[i]
            tuple_list = []
            tuple_list.append(curr_items)
            tuple_list.append(ner_tag)
            ner_prediction.append(tuple_list)
        i = i + 1

    return ner_prediction
    # for tup in ner_prediction:
    #     print(tup)


# Ambil smua yang ke tagged_named_entity
# Bandingin sama yang sama (person dgn person) dah trus baru itung co-occurence terbesarnya
def co_occurence_calculation(username, ner_prediction):
    # Kasi kasus disini, kalo dia location dibandingin ama attribut mana aja di user profil, dkk
    user_dict = fetch_user_profile.get_data(username)
    # print(user_dict)
    predicted_sentence_cooccurence = []

    i = 0
    for chunk_tuple in ner_prediction:
        co_occurence = 0
        # print(chunk_tuple[1])
        if ("per" == chunk_tuple[1]):
            # Compare with full name
            co_occurence = google_search.co_occurence(user_dict['full_name'], chunk_tuple[0])
        elif ("org" == chunk_tuple[1]):
            # Compare with education, work
            co_occurence_1 = google_search.co_occurence(user_dict['education'], chunk_tuple[0])
            co_occurence_2 = google_search.co_occurence(user_dict['work'], chunk_tuple[0])
            if (co_occurence_1 > co_occurence_2):
                co_occurence = co_occurence_1
            else:
                co_occurence = co_occurence_2
        elif ("geo" == chunk_tuple[1]):
            # Compare with hometown_city, current_city,
            co_occurence_1 = google_search.co_occurence(user_dict['hometown_city'], chunk_tuple[0])
            co_occurence_2 = google_search.co_occurence(user_dict['current_city'], chunk_tuple[0])
            if (co_occurence_1 > co_occurence_2):
                co_occurence = co_occurence_1
            else:
                co_occurence = co_occurence_2

        predicted_sentence_cooccurence.append(co_occurence)

    # print(predicted_sentence_cooccurence)
    return predicted_sentence_cooccurence

def simple_anonymize(ner_prediction):
    anonymize_predicted_sentence = anonymization.simple_anonymization(ner_prediction)
    final_sentence = postprocessing.restructure_sentence(anonymize_predicted_sentence)
    return final_sentence

def compute_similarity(text_input, final_sentence):
    print('Original text : ')
    print(text_input)
    print('Anonymized text : ')
    print(final_sentence)

    print('Similarity : ')
    print(sentence_similarity.symmetric_sentence_similarity(text_input, final_sentence))

# Buat yang alphanya di bawah threshold (co-occurencenya kecil), di cek lagi sama rule based approach
# loc_candidate_phrases = sample_rule_based.identify_candidate_private_locational_phrases(ner_prediction)
def identify_private_locational_phrases(normalized_tokenized_output, level):
    all_idx = sample_rule_based.private_locational_main_function(normalized_tokenized_output)
    anonymized_loc_sentence = location_generalization.anonymize_all_location(normalized_tokenized_output, all_idx, level)
    return anonymized_loc_sentence

def identify_private_personal_phrases(normalized_tokenized_output):
    all_idx = sample_rule_based.private_personal_main_function(normalized_tokenized_output)
    anonymized_per_sentence = genderize.anonymize_all_person(normalized_tokenized_output, all_idx)
    return anonymized_per_sentence

def identify_private_organizational_phrases(normalized_tokenized_output):
    org_candidate_phrases = sample_rule_based.identify_candidate_private_organizational_phrases(ner_prediction)
    print('Step 3b : ')
    print(org_candidate_phrases)
    non_neg_org_candidate_phrases = sample_rule_based.check_negative_phrases(org_candidate_phrases)
    print('Step 4b : ')
    print(non_neg_org_candidate_phrases)
    private_org_candidate_phrases = sample_rule_based.check_non_private_organizational_verb(non_neg_org_candidate_phrases)
    print('Step 5b : ')
    print(private_org_candidate_phrases)
    truly_private_org_candidate_phrases = sample_rule_based.check_private_organizational_verb(private_org_candidate_phrases)
    print('Step 6b : ')
    print(truly_private_org_candidate_phrases)

def identify_private_temporal_phrases(message):
    # message = ""
    # i = 0
    # for tuples in ner_prediction:
    #     message = message + tuples[0]
    #     i = i + 1
    #     if (i < len(pos_tagged_input)):
    #         message = message + " "

    message = temporal_phrase_tagger.do_temporal_tag(message)

    # Anonymization here

    return message

if __name__ == '__main__':
    # python main.py load save_model_crf_gmb_dua_kali.pkl "On June 24th, I went to Bali for vacation" "Geraldi Dzakwan"
    # python main.py load save_model_crf_gmb_dua_kali.pkl "My sister's name is Alice. Alice lives in Jakarta." "Geraldi Dzakwan"
    # python main.py load save_model_crf_gmb_dua_kali.pkl "I live in Jakarta with my sister, Alice." "Geraldi Dzakwan"

    if(len(sys.argv) < 5):
        sys.exit('Wrong arguments')

    crf = None
    if(sys.argv[1] == 'load'):
        crf = load_or_train_crf(True, sys.argv[2])
    elif(sys.argv[1] == 'save'):
        crf = load_or_train_crf(False, sys.argv[2])
    else:
        sys.exit('Wrong 1st arguments')

    input_message = sys.argv[3]
    pos_tagged_input = do_pos_tag(input_message)
    featured_input = extract_features(pos_tagged_input)
    iob_prediction = predict_named_entity(crf, featured_input)
    ner_prediction = combine_named_entity_chunks(pos_tagged_input, iob_prediction)
    predicted_sentence_cooccurence = co_occurence_calculation(sys.argv[4], ner_prediction)

    print(pos_tagged_input)
    print('----------')
    print(iob_prediction)
    print('----------')
    print(ner_prediction)
    print('----------')
    print(predicted_sentence_cooccurence)
    print('----------')
    print(identify_private_locational_phrases(ner_prediction, 1))
    print('----------')
    # identify_private_organizational_phrases(ner_prediction)
    # print('----------')
    print(identify_private_personal_phrases(ner_prediction))
    print('----------')
    # identify_private_temporal_phrases(input_message)

    # Ntar disatuin ama threshold dan co-occurence yang LOC sama ORG besok
    # PERSON pikirin lagi
    # Time/temporal phrase di akhir aja
