# Main library used for natural language processing (natural language toolkit)
import nltk
# Download all basic corpora and library as used in the book
# nltk.download('book')

# Function to eliminate unnecessary things like '(', ')', ',', etc
def text_preprocessing(text):
    # This is used to parse betweens sentences
    sentences = nltk.sent_tokenize(text)

    # Debugging
    # print(sentences)

    # This is used to parse between words in each sentence
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

    # Debugging
    # print(tokenized_sentences)

    # This is used to do post tagging for each word
    tagged_sentences = [nltk.pos_tag(word) for word in tokenized_sentences]

    # Debugging
    # print(tagged_sentences)

    return tagged_sentences

# Function to return tagged text from processed text
def text_ner_tagging(tagged_sentences):
    # This is used to do NER tagging for each word
    # Binary = True means it will only detect whether a word has named entity
    # Binary = False means it will also detect the class of a word which has named entity
    chunked_sentences = [nltk.ne_chunk(word, binary=False) for word in tagged_sentences]

    # Debugging
    # print(chunked_sentences)

    # This will be the output of NER processing
    processed_list = []
    # chunked_sentences is a tree with root node containing sentences
    # So, we should get what's inside the root node
    inside_chunked_sentences = chunked_sentences[0]
    iterator_1 = 0

    #Loop through all the words
    while(iterator_1 < len(inside_chunked_sentences)):
        # Debugging
        # print(inside_chunked_sentences[iterator_1])

        whole_word = ""
        whole_label = "None"

        # Check if it contains named entity label
        if (type(inside_chunked_sentences[iterator_1]) == nltk.tree.Tree):
            # Later check for case there is 'of' between named entity (between Tree)
            # e.g. United States of
            is_tree = False
            while(type(inside_chunked_sentences[iterator_1]) == nltk.tree.Tree):
                # If it is a named entity, add the right label/class to the tuple
                # Group all consecutive same named entity
                # Check also if a tree has more than one item, e.g. : Tree('ORGANIZATION', [('Real', 'NNP'), ('Madrid', 'NNP')])

                temp_word = inside_chunked_sentences[iterator_1][0][0]
                first = True
                for word_tuple in inside_chunked_sentences[iterator_1]:
                    if(not first):
                        temp_word += " "
                        temp_word += word_tuple[0]
                    first = False

                whole_word += temp_word
                whole_word += " "

                whole_label = inside_chunked_sentences[iterator_1].label()

                # processed_list.append([inside_chunked_sentences[iterator_1][0][0], inside_chunked_sentences[iterator_1].label()])
                # processed_list.append([temp_word, inside_chunked_sentences[iterator_1].label()])

                # Debugging
                # print(inside_chunked_sentences[iterator_1][0][0], inside_chunked_sentences[iterator_1].label())

                # whole_word += inside_chunked_sentences[iterator_1][0][0]

                # Debugging
                # print('To NER : ', inside_chunked_sentences[iterator_1][0][0])

                is_tree = True

                iterator_1 = iterator_1 + 1


        if (is_tree):
            processed_list.append([whole_word, whole_label])

        # Debugging
        # print('DELIMITER CHUNK')

        # print(inside_chunked_sentences[iterator_1-1]);
        # processed_list.append([whole_word, inside_chunked_sentences[iterator_1-1].label()])

        # If it is not a named entity, add None label to the tuple
        processed_list.append([inside_chunked_sentences[iterator_1][0], None])

        # Debugging
        # print('To other : ', inside_chunked_sentences[iterator_1][0])

        iterator_1 = iterator_1 + 1

    # NOTES
    # Alternative : Detect all nouns, manually tag the named entity

    # Debugging
    # print(processed_list)

    return processed_list

# Function to do text anonymization based on parameter supplied
def text_anonymization(processed_list, anonymization_type):
    if(anonymization_type == 'general'):
        list_len = len(processed_list)
        i = 0
        count_person = 0;
        count_organization = 0;
        count_gpe = 0;

        while(i < list_len):
            if(processed_list[i][1] != 'None'):
                if(processed_list[i][1] == 'PERSON'):
                    count_person = count_person + 1
                    processed_list[i][0] = 'PERSON' + '-' + str(count_person)
                elif(processed_list[i][1] == 'ORGANIZATION'):
                    count_organization = count_organization + 1
                    processed_list[i][0] = 'ORG' + '-' + str(count_organization)
                elif(processed_list[i][1] == 'GPE'):
                    count_gpe = count_gpe + 1
                    processed_list[i][0] = 'GPE' + '-' + str(count_gpe)

            i = i + 1

        return processed_list
    else:
        return 'to be defined'

# if __name__ == "__main__":
#     # Text input from stdio
#     text = raw_input()
#
#     if (text == 'default'):
#         # text = "Barack Obama is a great person in United States of America and Great Britain. He is truly our president."
#         # Bugs here
#         # text = "Cristiano Ronaldo is a decent footballer both in Spain (Real Madrid) and United Kingdom (Manchester United). He is truly a masterpiece."
#         # text = "Cristiano Ronaldo is a decent footballer both in Real Madrid, Spain and Manchester United, Great Britain. He is truly a masterpiece."
#         # text = "Cristiano Ronaldo is a decent footballer both in Real Madrid."
#         text = "Cristiano Ronaldo is a decent footballer both in Real Madrid, Spain and Manchester United, United Kingdom. He is truly a masterpiece."
#
#     tagged_sentences = text_preprocessing(text)
#
#     # Debugging
#     # for sentence in tagged_sentences:
#     #     for word in sentence:
#     #         print(word)
#     #     print('Next sentence : ')
#
#     processed_list = text_ner_tagging(tagged_sentences)
#
#     # Debugging
#     for item in processed_list:
#         print(item)
#
#     anonymized_list = text_anonymization(processed_list, 'general')
#
#     # Debugging
#     # for item in anonymized_list:
#     #     print(item)
