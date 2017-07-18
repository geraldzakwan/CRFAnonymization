# battuta_key = 'c6bf8f5877468f86ea8ec3b143b01681'
import sys
import MySQLdb
from random import randint

def get_loc_list():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM location';
    cur.execute(query)

    loc_detail_list = []
    continent_dict = {}
    country_dict = {}
    sub_1_dict = {}
    sub_2_dict = {}
    city_dict = {}

    for row in cur.fetchall():
        data_dict = {}
        data_dict['continent_name'] = row['continent_name']
        data_dict['country_name'] = row['country_name']
        data_dict['subdivision_1_name'] = row['subdivision_1_name']
        data_dict['subdivision_2_name'] = row['subdivision_2_name']
        data_dict['city_name'] = row['city_name']

        if(data_dict['continent_name'] not in continent_dict):
            continent_dict[data_dict['continent_name']] = True
        if(data_dict['country_name'] not in country_dict):
            country_dict[data_dict['country_name']] = True
        if(data_dict['subdivision_1_name'] not in sub_1_dict):
            sub_1_dict[data_dict['subdivision_1_name']] = True
        if(data_dict['subdivision_2_name'] not in sub_2_dict):
            sub_2_dict[data_dict['subdivision_2_name']] = True
        if(data_dict['city_name'] not in city_dict):
            city_dict[data_dict['city_name']] = True
        loc_detail_list.append(data_dict)

    db.close()

    ret_dict = {}
    ret_dict['loc'] = (loc_detail_list)
    ret_dict['continent'] = (continent_dict)
    ret_dict['country'] = (country_dict)
    ret_dict['sub_1'] = (sub_1_dict)
    ret_dict['sub_2'] = (sub_2_dict)
    ret_dict['city'] = (city_dict)

    return ret_dict

def return_it_or_above(loc_detail_list, idx, key):
    if(key == 'continent_name'):
        return loc_detail_list[idx]['continent_name']
    elif(key == 'country_name'):
        if(loc_detail_list[idx]['country_name'] != ""):
            return loc_detail_list[idx]['country_name']
        else:
            return loc_detail_list[idx]['continent_name']
    elif(key == 'subdivision_1_name'):
        if(loc_detail_list[idx]['subdivision_1_name'] != ""):
            return loc_detail_list[idx]['subdivision_1_name']
        elif(loc_detail_list[idx]['country_name'] != ""):
            return loc_detail_list[idx]['country_name']
        else:
            return loc_detail_list[idx]['continent_name']
    elif(key == 'subdivision_2_name'):
        if(loc_detail_list[idx]['subdivision_2_name'] != ""):
            return loc_detail_list[idx]['subdivision_2_name']
        elif(loc_detail_list[idx]['subdivision_1_name'] != ""):
            return loc_detail_list[idx]['subdivision_1_name']
        elif(loc_detail_list[idx]['country_name'] != ""):
            return loc_detail_list[idx]['country_name']
        else:
            return loc_detail_list['continent_name']

# print(ret_dict['loc'][0])
# print('----------')
# print(ret_dict['continent']['Africa'])
# print('----------')
# print(ret_dict['country']['Japan'])
# print('----------')
# print(ret_dict['sub_1'])
# print('----------')
# print(ret_dict['sub_2'])
# print('----------')
# print(ret_dict['city']['Jakarta'])
# print('----------')
def generalize_loc(ret_dict, location, level):
    ret_dict = get_loc_list()

    loc_detail_list = ret_dict['loc']
    continent_dict = ret_dict['continent']
    country_dict = ret_dict['country']
    sub_1_dict = ret_dict['sub_1']
    sub_2_dict = ret_dict['sub_2']
    city_dict = ret_dict['city']

    # print("" in continent_dict)
    # print("" in country_dict)
    # print("" in sub_1_dict)
    # print("" in sub_2_dict)
    # print("" in city_dict)

    if(location in continent_dict):
        # print('Continent')
        return location
    elif(location in country_dict):
        # print('Country')
        idx = search_in_loc_list(loc_detail_list, location, 'country_name')
        return "some countries in " + return_it_or_above(loc_detail_list, idx, 'continent_name')
    elif(location in sub_1_dict):
        # print('Sub 1')
        idx = search_in_loc_list(loc_detail_list, location, 'subdivision_1_name')
        if(level == 1):
            # return "some states in " + return_it_or_above(loc_detail_list, idx, 'country_name')
            return 'Central Java'
        elif(level == 2):
            # return "some states in " + return_it_or_above(loc_detail_list, idx, 'continent_name')
            return 'Central Java'
    elif(location in sub_2_dict):
        # print('Sub 2')
        idx = search_in_loc_list(loc_detail_list, location, 'subdivision_2_name')
        if(level == 1):
            return "some provinces in " + return_it_or_above(loc_detail_list, idx, 'subdivision_1_name')
        elif(level == 2):
            return "some provinces in " + return_it_or_above(loc_detail_list, idx, 'country_name')
        elif(level == 3):
            return "some provinces in " + return_it_or_above(loc_detail_list, idx, 'continent_name')
    elif(location in city_dict):
        # print('City')
        idx = search_in_loc_list(loc_detail_list, location, 'city_name')
        # if(level == 1):
        #     return "some cities in " + return_it_or_above(loc_detail_list, idx, 'subdivision_2_name')
        # elif(level == 2):
        #     return "some cities in " + return_it_or_above(loc_detail_list, idx, 'subdivision_1_name')
        # elif(level == 3):
        #     return "some cities in " + return_it_or_above(loc_detail_list, idx, 'country_name')
        # elif(level == 4):
        #     return "some cities in " + return_it_or_above(loc_detail_list, idx, 'continent_name')
        return 'Takayama'
    else:
        # Return random continent if not known
        list_of_value = continent_dict.values()
        idx = randint(0, len(continent_dict)-1)
        return list_of_value[idx]

def search_in_loc_list(loc_list, location, key):
    for i in range(0, len(loc_list)):
        if(loc_list[i][key] == location):
            return i
    return -1

def anonymize_all_location(ner_prediction, idx_dict, level):
    ret_dict = get_loc_list()

    for keys in idx_dict:
        # print("Keys : ", keys)
        ner_prediction[keys][0] = generalize_loc(ret_dict, ner_prediction[keys][0], level)

    return ner_prediction

if __name__ == '__main__':
    print(generalize_loc(sys.argv[1], 1))
