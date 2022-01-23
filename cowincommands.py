import requests
import json

import json
import json

with open('states.json', 'r+') as dingo:
    data = json.loads(dingo.read())


def getpin(pin, date):
    # https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode=110001&date=31-03-2021
    params = {
        'pincode': pin,
        'date': date
    }
    a = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin', params=params).json()
    if a['sessions']:
        print(a['sessions'])
        return a['sessions']
    else:
        return []


#         for i in a['sessions']:
#             x = "\n        ".join(i['slots'])
#             return (f'''
# Centre name : {i['name']}
# Address : {i['address']}
# Slots:  {x}
# Vaccine : {i['vaccine']}
# Fee : {i['fee']}
# Minimum Age : {i['min_age_limit']}
#             ''')
#     else:
#         return "No sessions available for your pin code."


def getdist(district, state, date):
    base_url = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/'

    did = -1
    for i in requests.get(base_url + data[state.lower()]).json()['districts']:
        if i['district_name'].lower() == district.lower():
            did = i['district_id']
            break
    if did == -1:
        return "District not found"
    else:
        a2 = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict',
                          params={'district_id': str(did), 'date': date}).json()
        # print(a2)
        if a2['sessions']:
            return a2['sessions']
            # for i in a2['sessions']:
            # print(i)
            # x = "\n        ".join(i['slots'])
        #                 return (f'''
        # Centre name : {i['name']}
        # Address : {i['address']}
        # Slots:  {x}
        # Vaccine : {i['vaccine']}
        # Fee : {i['fee']}
        # Minimum Age : {i['min_age_limit']}
        #                     ''')
        else:
            return "Please try again"

# print(getdist('alappuzha','kerala','24-01-2022'))
