from urllib.request import urlopen
import json

def get_codes():
    url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=8f714b6f-c35c-4b40-a0e7-547b675eee0e&fields=city_name_he,city_code'  
    response = urlopen(url)
    jsonResponse = json.loads(response.read().decode('utf-8'))
    settlements = jsonResponse['result']['records']
    settlementsDict = {}
    for i in settlements:
        settlementsDict[i['city_name_he'][:-1]] = i['city_code']
    return settlementsDict


if __name__ == '__main__':
    print(get_codes())