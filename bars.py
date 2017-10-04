import sys
import json
import math


def load_data(filepath):
    with open(filepath, 'r', encoding='windows-1251') as file_descriptor:
        file_contents = file_descriptor.read()
    file_descriptor.close()
    return file_contents


def calculate_geo_distance(from_longitude, from_latitude, to_longitude, to_latitude):
    return math.sqrt((to_longitude - from_longitude) ** 2 + (to_latitude - from_latitude) ** 2)


def get_biggest_bar(json_contents):
    bars = json.loads(json_contents)
    biggest_bar = None
    for bar in bars:
        if not biggest_bar or \
                (int(bar['SeatsCount']) > int(biggest_bar['SeatsCount']) and int(bar['SeatsCount']) > 0):
            biggest_bar = bar
    return biggest_bar


def get_smallest_bar(json_contents):
    bars = json.loads(json_contents)
    smallest_bar = None
    for bar in bars:
        if not smallest_bar or \
                (int(bar['SeatsCount']) < int(smallest_bar['SeatsCount']) and int(bar['SeatsCount']) > 0):
            smallest_bar = bar
    return smallest_bar


def get_closest_bar(json_contents, user_latitude, user_longitude):
    bars = json.loads(json_contents)
    closest_bar = None
    for bar in bars:
        if closest_bar == None or \
           calculate_geo_distance(float(bar['geoData']['coordinates'][0]),
                                  float(bar['geoData']['coordinates'][1]),
                                  float(user_latitude),
                                  float(user_longitude))\
                        < \
           calculate_geo_distance(float(closest_bar['geoData']['coordinates'][0]),
                                  float(closest_bar['geoData']['coordinates'][1]),
                                  float(user_latitude),
                                  float(user_longitude)):
           closest_bar = bar
    return closest_bar


def print_bar(bar):
    if bar:
        print(u'Found bar: {}, address: {}, phone: {}, seats {}, latitude: {}, longtitude: {}'.format(
            bar['Name'],
            bar['Address'],
            bar['PublicPhone'][0]['PublicPhone'],
            bar['SeatsCount'],
            bar['geoData']['coordinates'][0],
            bar['geoData']['coordinates'][1]
        ))
    else:
        print('Bar not found')

def get_argv_or_exit():
    if len(sys.argv) < 3 or sys.argv[1] == '--help':
        print(u'JSON Bars analyzer')
        print(u'Usage python bars.py filename type[ latitude longtitude]')
        print(u'Where type in [\'biggest\', \'smallest\', \'closest\']')
        print(u'For closest add latitude and longtitude coordinates')
        sys.exit(0)
    if sys.argv[2] == 'closest' and len(sys.argv) < 5:
        print(u'For closest add latitude and longtitude coordinates')
        sys.exit(0)
    if sys.argv[2] not in ['biggest', 'smallest', 'closest']:
        print(u'Unkown type {}. Please one use from [\'biggest\', \'smallest\', \'closest\']'.format(type))
    params = {'filepath': sys.argv[1], 'type': sys.argv[2], 'user_latitude': None, 'user_longitude': None}
    if sys.argv[2] == 'closest':
        params['user_latitude'] = sys.argv[3]
        params['user_longitude'] = sys.argv[4]
    return params


def find_bars(filepath, type, user_latitude = None, user_longitude = None):
    json_contents = load_data(filepath)
    if type == 'biggest':
        print_bar(get_biggest_bar(json_contents))
    elif type == 'smallest':
        print_bar(get_smallest_bar(json_contents))
    elif type == 'closest':
        print_bar(get_closest_bar(json_contents, user_latitude, user_longitude))


if __name__ == '__main__':
    params = get_argv_or_exit()
    find_bars(**params)
    sys.exit(0)
