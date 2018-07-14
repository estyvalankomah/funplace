#!/usr/bin/python
"""Small search Engine For accessing foursquare"""

import json

from requests import request

GAK = ''
# GAK = '&key=AIzaSyD4QCanvCVjqVfR_BVkA8h5BOI7W95TUaE' #GOOGLE API KEY

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

    for i in range(5):  # try for max of 5 times
        try:
            response = request('GET',
                               f'https://maps.googleapis.com/maps/api/geocode/json?address={address}{GAK}')
            response = json.loads(response.text)
            lat = response['results'][0]['geometry']['location']['lat']
            lng = response['results'][0]['geometry']['location']['lng']
            return lat, lng
        except KeyError:
            print('WARNING: geocode failed! Trying Again...')
            continue

    return 0, 0  # A default lat,lang so the foursqurae doesn't crash


def search_foursquare(lat, lng) -> dict:
    """Gets Hottest place info from foursquare API
    :rtype: dict
    """

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

    return data


def search(address):
    """Given an addres, it geocodes the adddress and calls search_foursquare
    :rtype: dict
    """
    lat, lng = geocode(address)
    response = search_foursquare(lat, lng)
    return response


def get_item_list(response):
    """Get place Item list of places from the foursquare response"""
    place_list = response['response']['groups'][0]['items']
    assert isinstance(place_list, list)
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
