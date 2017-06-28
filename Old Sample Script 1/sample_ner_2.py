import nltk

# nltk.download('treebank')
# nltk.download('book')

sent = "They saw me in Japan"
sent = nltk.word_tokenize(sent) #to identify word in a sentence
sent = nltk.pos_tag(sent)       #to identify the parts of speech
sent = nltk.ne_chunk(sent)

# for sen1 in sent:
#     for sen2 in sen1:
#         print(sen2)
#     if (hasattr(sen1, 'node'))  :
#         print('Node : ', sen1.node)

print(sent[4].label())
