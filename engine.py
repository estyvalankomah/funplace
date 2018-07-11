from requests import request
import json
import sys

GAK=''
#GAK = '&key=AIzaSyD4QCanvCVjqVfR_BVkA8h5BOI7W95TUaE' #GOOGLE API KEY

address = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'
if len(sys.argv)>1:
    address = sys.argv[1]
    address = address.strip(' ').split(' ')
    address = '+'.join(address)


res = request('GET', 'https://maps.googleapis.com/maps/api/geocode/json?address={}{}'.format(address,GAK))
res_dict = json.loads(res.text)
lat = res_dict['results'][0]['geometry']['location']['lat']
lng = res_dict['results'][0]['geometry']['location']['lng']


url = 'https://api.foursquare.com/v2/venues/explore'

params = dict(
  client_id='IZYMTGJNI3PUUV0B4XJB1I3XSQEYFJLRD0PQE5XTB3L5A2FS',
  client_secret='XEGRP41ZP1SS3RJPMSM3YLWFIXVYHQZZRLFF0FG3V1O4ODHQ',
  v='20180323',
  ll='{},{}'.format(lat, lng),
  section='topPicks',
  limit=10
)
resp = request('GET', url=url, params=params)
data = json.loads(resp.text)
print(data)

print(lat, lng)
print(
    'https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(address), 
    sep='\n'
    )