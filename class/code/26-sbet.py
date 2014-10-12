#!/usr/bin/env python

'''Decode Applanix POSPac SBET IMU binary files

Starting point for Class 26.
'''

import struct
import math
# Use the pprint function from the pprint module
from pprint import pprint

field_names = ('time', 'latitude', 'longitude', 'altitude', \
          'x_vel', 'y_vel', 'z_vel', \
          'roll', 'pitch', 'platform_heading', 'wander_angle', \
          'x_acceleration', 'y_acceleration', 'z_acceleration', \
          'x_angular_rate', 'y_angular_rate', 'z_angular')

datagram_size = 136 # 8*17 bytes per datagram

def num_datagrams(data):
    'How many packets are in data'

    assert( len(data) % datagram_size == 0 )

    return len(data) / datagram_size

def get_offset(datagram_number):
    'Calculate the starting offset of a datagram.  First datagram is number 0'
    return datagram_number * datagram_size

def decode(data, offset=0):
    'Decipher a SBET datagram from binary'
    values = struct.unpack('17d',data[ offset + 0 : offset + 8*17])

    sbet_values = dict(zip (field_names, values))

    sbet_values['lat_deg'] = math.degrees(sbet_values['latitude'])
    sbet_values['lon_deg'] = math.degrees(sbet_values['longitude'])

    return sbet_values

def load_sbet_file(filename):
    '''This is a GENERATOR that we can loop over with a for'''
    sbet_file = open(filename)
    sbet_data = sbet_file.read()

    for datagram_index in range( num_datagrams(sbet_data) ):
        offset = get_offset(datagram_index)
        datagram = decode(sbet_data, offset)
        datagram['index'] = datagram_index
        yield datagram
        
def main():
    import glob
    import sys

    print 'Starting main'

    import sys, argparse

    parser = argparse.ArgumentParser(description='Parse SBET files')
    parser.add_argument('filenames', type=str, nargs='+', help='SBET files')
    args = parser.parse_args() # uses sys.argv

    print 'filenames:', args.filenames

    for filename in args.filenames:
        print '====',filename,'===='
        out = open(filename+'.kml', 'w')
        out.write('''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
            <Placemark>
                    <name>{filename}</name>
                    <LineString>
                            <coordinates>
        '''.format(filename=filename) )

        print 'Datagram Number, Time, x, y'
        for datagram_index, datagram in enumerate(load_sbet_file( filename )):
            if datagram_index % 20 == 0:
                print datagram_index, datagram['time'], datagram['lon_deg'], datagram['lat_deg']
            out.write('{x},{y}\n'.format(x=datagram['lon_deg'], y=datagram['lat_deg']))

        out.write('''\t\t\t\t</coordinates>
\t\t\t</LineString>
\t\t</Placemark>
\t</Document>
</kml>
        ''')

    
if __name__ == '__main__':
    print 'starting to run script...'
    main()
    print 'script done!'
