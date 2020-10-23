import requests
import json
import csv
import os
def get_businesses(location, term, api_key):
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/search'
    data = []
    for offset in range(0, 1000, 50):
        params = {
            'limit': 50,
            'location': location.replace(' ', '+'),
            'term': term.replace(' ', '+'),
            'offset': offset
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data += response.json()['businesses']
        elif response.status_code == 400:
            print('400 Bad Request')
            break
    return data

api_key = 'xUPRVd5yhRVN_gfRSNucGzRoLxusNFMHRJ6X57rn40AEPvv762eOf_3FlQ3Zy1sy9KNNhbZu40IevRJBzTe9L5-V9c44fu8rg7amf0Qc6j5oX75z3ZwJW8WYSsGiXHYx'
term='restaurant'
location='Atlanta'

businesses=get_businesses(location, term, api_key)
print(len(businesses))

# for business in businesses:
#     print("Name:", business["name"])
#     print("Rating:", business["rating"])
#     print("zip_code:", business["location"]["zip_code"])
#     print('')
# with open("Yelp.csv", "w", encoding='utf-8', newline='') as f:
#     writer = csv.writer(f, delimiter=',')
#     writer.writerow(["Name", "zip_code"])
#     for business in businesses:
#         writer.writerow([business["name"], business["location"]["zip_code"]])
#     f.close()
