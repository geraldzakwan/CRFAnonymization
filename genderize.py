import requests, json

def get_name_list():
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="root",         # your username
                         passwd="",  # your password
                         db="english_corpus")        # name of the data base

    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # Use all the SQL you like
    query = 'SELECT * FROM name_corpus';
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

def getGenders(names):
	url = ""
	cnt = 0
	if not isinstance(names,list):
		names = [names,]

	for name in names:
		if url == "":
			url = "name[0]=" + name
		else:
			cnt += 1
			url = url + "&name[" + str(cnt) + "]=" + name


	req = requests.get("https://api.genderize.io?" + url)
	results = json.loads(req.text)

	retrn = []
	for result in results:
		if result["gender"] is not None:
			retrn.append((result["gender"], result["probability"], result["count"]))
		else:
			retrn.append((u'None',u'0.0',0.0))

	return retrn

if __name__ == '__main__':
	print(getGenders(["Brian","Atika","Jessica","Zaeem","NotAName"]))
