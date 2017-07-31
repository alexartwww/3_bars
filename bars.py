# -*- coding: utf-8 -*-

import sys
import json
import math


def load_data(filepath):
    file_descriptor = open(filepath, "r")
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
                (bar['SeatsCount'] > biggest_bar['SeatsCount'] and bar['SeatsCount'] > 0):
            biggest_bar = bar
    return biggest_bar


def get_smallest_bar(json_contents):
    bars = json.loads(json_contents)
    smallest_bar = None
    for bar in bars:
        if not smallest_bar or \
                (bar['SeatsCount'] < smallest_bar['SeatsCount'] and bar['SeatsCount'] > 0):
            smallest_bar = bar
    return smallest_bar


def get_closest_bar(json_contents, user_latitude, user_longitude):
    bars = json.loads(json_contents)
    closest_bar = None
    for bar in bars:
        if closest_bar == None or \
           calculate_geo_distance(bar['geoData']['coordinates'][0],
                                  bar['geoData']['coordinates'][1],
                                  user_latitude,
                                  user_longitude)\
                        < \
           calculate_geo_distance(closest_bar['geoData']['coordinates'][0],
                                  closest_bar['geoData']['coordinates'][1],
                                  user_latitude,
                                  user_longitude):
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


if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] == '--help':
        print(u'JSON Bars analyzer')
        print(u'Usage python bars.py filename type[ latitude longtitude]')
        print(u'Where type in [\'biggest\', \'smallest\', \'closest\']')
        print(u'For closest add latitude and longtitude coordinates')
        sys.exit(0)

    json_contents = load_data(sys.argv[1])
    json_contents = json_contents.decode('windows-1251').encode('utf-8')
    type = sys.argv[2]
    if type == 'biggest':
        print_bar(get_biggest_bar(json_contents))
    elif type == 'smallest':
        print_bar(get_smallest_bar(json_contents))
    elif type == 'closest':
        if len(sys.argv) < 5:
            print(u'For closest add latitude and longtitude coordinates')
            sys.exit(0)
        else:
            user_latitude = float(sys.argv[3])
            user_longitude = float(sys.argv[4])
            print_bar(get_closest_bar(json_contents, user_latitude, user_longitude))
    else:
        print(u'Unkown type {}. Please use from [\'biggest\', \'smallest\', \'closest\']'.format(type))
    sys.exit(0)
