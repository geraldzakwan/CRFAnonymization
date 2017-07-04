from apiclient.discovery import build

api_key = 'AIzaSyDkSCA8agvst49gtKEjrxRnI57lCqV9vBM'
cx_key = '013692161269702497108:vgnkfyixhmo'

def get_total_results():
    service = build("customsearch", "v1", developerKey=api_key)

    res = service.cse().list(q='Tokyo AND Kyoto', cx=cx_key,).execute()

    total_results = res['queries']['request'][0]['totalResults']

    print(total_results)

    res = service.cse().list(q='Tokyo OR Kyoto', cx=cx_key,).execute()

    total_results = res['queries']['request'][0]['totalResults']

    print(total_results)

    # return total_results

if __name__ == '__main__':
    # print(get_total_results())
    get_total_results()
