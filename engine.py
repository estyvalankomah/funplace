#!/usr/bin/python

"""Small search Engine For accessing foursquare"""

from requests import request
import json
import sys

GAK=''
#GAK = '&key=AIzaSyD4QCanvCVjqVfR_BVkA8h5BOI7W95TUaE' #GOOGLE API KEY

ADDRESS = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'

"""
#for command line compatibility
if len(sys.argv)>1:
    address = sys.argv[1]
    address = address.strip(' ').split(' ')
    address = '+'.join(address)
"""

def geocode(address):
    """Takes an address and returns the coordinate of it"""
    
    for i in range(5): #try for max of 5 times
        is_successful = False #will be set to true if geocoded succesfully
        try:
            res = request('GET', 'https://maps.googleapis.com/maps/api/geocode/json?address={}{}'.format(address,GAK))
            res_dict = json.loads(res.text)
            lat = res_dict['results'][0]['geometry']['location']['lat']
            lng = res_dict['results'][0]['geometry']['location']['lng']
            is_successful = True
            break
        except:
            print('WARNING: geocode failed! Trying Again...')
            continue
    if is_successful:
        return lat,lng
    else:
        return 0,0 #A default lat,lang so the foursqurae doesn't crash


def search_foursquare(lat,lng):
    """Gets Hottest place info from foursquare API"""
    
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
    data = json.load(resp.text)
    
    return data


def search(address):
    """Given an addres, it geocodes the adddress and calls search_foursquare"""
    lat, lng = geocode(address)
    res_dict = search_foursquare(lat, lng)
    return res_dict
    
    
 def get_item_list(res_dict):
	 """Get place Item list of places from the foursquare response"""
	 place_list = res_dict['response']['groups'][0]['items']
	 return place_list

def clean(place_item):
	"""build a simpler dictionary of the place item"""
	cleaned_place_item = {}
	mapslink = ""
	try:
		cleaned_place_item['name'] = place_item['venue']['name']
		cleaned_place_item['category'] = place_item['categories'][0]['name']
		cleaned_place_item['address'] = place_item['venue']['location']['address']
		cleaned_place_item['mapslink'] = mapslink.format(
													place_item['venue']['location']['lat'],
													place_item['venue']['location']['lng']
												)
	except IndexError:
		print('WARNING: There was a problem cleaning the response')
		return place_item
		
	return cleaned_place_item

 def filter_results(result_dict):
	 place_list = get_item_list(result_dict)
	 cleaned_place_list = map(clean, place_list)
	 return cleaned_place_list
	 
	 

if __name__ == '__main__':
    res_dict = search(ADDRESS)
    print(res_dict)
    
    
    
    
