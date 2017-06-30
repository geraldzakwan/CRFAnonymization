with open('query_error_list_conll2002_ned.txt') as f:
    content = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

thefile = open('query_error_list_conll2002_ned_double_quotes.txt', 'w')
for item in content:
    first_single_quote = item.find("'")
    item = item[:87] + '"' + item[88:]

    i = first_single_quote
    char = item[i]

    while (char != ','):
        i = i + 1
        char = item[i]
    i = i - 1

    item = item[:i] + '"' + item[i+1:]

    item = item + ';'

    try:
        thefile.write("%s\n" % item)
    except:
        print(item)
