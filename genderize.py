import sys
import MySQLdb
import requests, json

def get_name_list():
    db = MySQLdb.connect(host="localhost",      # your host, usually localhost
                         user="root",           # your username
                         passwd="",             # your password
                         db="english_corpus")   # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM name_corpus';
    cur.execute(query)
    ret_dict = {}
    ret_dict['+'] = []
    ret_dict['-'] = []

    for row in cur.fetchall():
        ret_dict[row['gender']].append(row['word'])

    db.close()
    return ret_dict

def get_first_name(name):
    first_name = ""
    for i in range(0, len(name)):
        if(name[i] == " "):
            break
        else:
            first_name = first_name + name[i]

    return first_name

def get_genders(names):
    url = ""
    cnt = 0
    if not isinstance(names, list):
        names = [names,]

    for name in names:
        first_name = get_first_name(name)
        if url == "":
            url = "name[0]=" + first_name
        else:
            cnt += 1
            url = url + "&name[" + str(cnt) + "]=" + first_name

    req = requests.get("https://api.genderize.io?" + url)
    results = json.loads(req.text)

    retrn = []

    for result in results:
        if(result["gender"] is not None):
            retrn.append((result["gender"], result["probability"], result["count"]))
        else:
            retrn.append((u'None',u'0.0',0.0))

    return retrn

if __name__ == '__main__':
    # print(get_name_list())
    if(len(sys.argv) < 2):
        sys.exit('Supply name')
    name_list = []
    for i in range(1, len(sys.argv)):
        name_list.append(sys.argv[i])
    print(get_genders(name_list))
