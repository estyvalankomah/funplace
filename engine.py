from requests import request
import json
import sys

#GOOGLE_API_KEY = 'AIzaSyD4QCanvCVjqVfR_BVkA8h5BOI7W95TUaE'
IAT = '18526f6fc81747e899a4df9c6d7a2334'#INSTAGRAM_ACCES_TOKEN
address = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'
if len(sys.argv)>1:
    address = sys.argv[1]
    address = address.strip(' ').split(' ')
    address = '+'.join(address)


try:
    res = request('GET', 'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(address))
    res_dict = json.loads(res.text)
    lat = res_dict['results'][0]['geometry']['location']['lat']
    lng = lat = res_dict['results'][0]['geometry']['location']['lng']
except IndexError:
    print('something went wrong, try again')

inst = request('GET', 'https://api.instagram.com/v1/media/search?lat={}&lng={}&client_id={}'.format(lat,lng,IAT))

print(inst.json())
print(lat, lng)