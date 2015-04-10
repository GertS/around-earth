import sys
import json
from pyorbital import tlefile
from pyorbital.orbital import Orbital
from datetime import datetime, timedelta


import time
import calendar

tle = tlefile.read('ISS (ZARYA)', 'stations.txt')

orb = Orbital('ISS (ZARYA)', 'stations.txt')

now = datetime.utcnow()
# Get normalized position and velocity of the satellite:
orb.get_position(now)
# Get longitude, latitude and altitude of the satellite:
position = orb.get_lonlatalt(now)

data = {}

timestamp = calendar.timegm(now.utctimetuple())
userLat = float(sys.argv[1])
userLng = float(sys.argv[2])
userAlt = float(sys.argv[3])

az, el = orb.get_observer_look(now, userLng, userLat, userAlt);

data['user_view'] = {}
data['user_view']['azimuth'] = az
data['user_view']['elevation'] = el

data['timestamp'] = timestamp

data['tle'] = {};
data['tle']['arg_perigee'] = orb.tle.arg_perigee
data['tle']['bstar'] = orb.tle.bstar
data['tle']['classification'] = orb.tle.classification
data['tle']['element_number'] = orb.tle.element_number
data['tle']['ephemeris_type'] = orb.tle.ephemeris_type
data['tle']['epoch'] = (orb.tle.epoch - datetime(1970, 1, 1)).total_seconds()
data['tle']['epoch_day'] = orb.tle.epoch_day
data['tle']['epoch_year'] = orb.tle.epoch_year
data['tle']['eccentricity'] = orb.tle.excentricity
data['tle']['id_launch_number'] = orb.tle.id_launch_number
data['tle']['id_launch_piece'] = orb.tle.id_launch_piece
data['tle']['id_launch_year'] = orb.tle.id_launch_year
data['tle']['inclination'] = orb.tle.inclination
data['tle']['mean_anomaly'] = orb.tle.mean_anomaly
data['tle']['mean_motion'] = orb.tle.mean_motion
data['tle']['mean_motion_derivative'] = orb.tle.mean_motion_derivative
data['tle']['mean_motion_sec_derivative'] = orb.tle.mean_motion_sec_derivative
data['tle']['orbit'] = orb.tle.orbit
data['tle']['right_ascension'] = orb.tle.right_ascension
data['tle']['satnumber'] = orb.tle.satnumber

SIDERAL_DAY_SEC = 86164.0905

data['tle']['orbit_time']  =  SIDERAL_DAY_SEC / orb.tle.mean_motion

data['position'] = {}
data['position']['longitude'] = position[0]
data['position']['latitude'] = position[1]
data['position']['altitude'] = position[2]


# calculate orbit line

halforbit = data['tle']['orbit_time'] / 2

start = timestamp - halforbit



from_date = now - timedelta(seconds=halforbit)
to_date = now + timedelta(seconds=halforbit)

# data['1'] = from_date.strftime("%Y-%m-%d %H:%M:%S")
# data['2'] = to_date.strftime("%Y-%m-%d %H:%M:%S")

delta=timedelta(minutes=1)


lineArray = []
while from_date <= to_date:

    onePointPosition = orb.get_lonlatalt(from_date)
    onePoint = {}
    onePoint['timestamp'] = start
    onePoint['longitude'] = onePointPosition[0]
    onePoint['latitude'] = onePointPosition[1]
    lineArray.append(onePoint);

    from_date = from_date + delta

data['orbit'] = lineArray

json_data = json.dumps(data)

print json_data