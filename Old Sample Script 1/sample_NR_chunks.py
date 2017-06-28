from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))

    print(chunked)
    prev = None
    continuous_chunk = []
    current_chunk = []

    named_entity_chunk = []

    # for i in chunked:
    #     if (type(i) == Tree):
    #         current_chunk.append(" ".join([token for token, pos in i.leaves()]))
    #         print(current_chunk)
    #     elif (current_chunk):
    #         print(current_chunk)
    #         named_entity = " ".join(current_chunk)
    #         # We need all the entity, even the same one
    #         # if named_entity not in continuous_chunk:
    #         continuous_chunk.append(named_entity)
    #         current_chunk = []
    #     # Not needed
    #     # else:
    #     #     continue
    #
    # # return continuous_chunk
    # return chunked

txt = "Barack Obama is a great person in United States of America and Great Britain. He is truly our president."
chunked = get_continuous_chunks(txt)

# for items in chunked:
#     print(items)
#     print('delimiter')
