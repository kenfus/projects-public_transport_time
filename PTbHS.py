import googlemaps
from datetime import datetime
import time
import urllib.request as ur
import werkzeug as wz
import json
import math
import pickle
import csv
import numpy as np
import gmaps
import gmaps.datasets
import pandas as pd

##This programm asks you for a destination and arrival-time. Then it makes a square around it (20 by 20 km)
##and puts the middle of a 250m*250m square as starting point into the
##Public Transport API of Google and saves the travel time for each query to a list.
##After getting the data, it maps the time with help of the gmaps-library and colors the points by the traveltime.
##I did this Programm to figure out places which are far away from Zürich (lower rent) but are still reachable in a passable time ##by train from the HB Zürich. With it's help, I found out about "Leimbach" and "Bachenbülach".


##TODO: The mapping still looks awful. Also there should be a way to run it without Jupyter Notebook.
##Also I figured out why Homegate or the others don't offer this: It's expensive to run! About 1600 Queries
##to Google (scales with n^2, n = amount of points checked).



api_key = 'AIzaSyDDRjczHB5nH28R7KLRVdepGpCa-fpdxcI' #INSERT YOUR GOOGLE API KEY HERE
gmaps.configure(api_key=api_key)
arrival_time = time.mktime(time.strptime(input('When do you have to be at work? 2015-10-20 22:24'), '%Y-%m-%d %H:%M'))
arrival_time = int(arrival_time)
print(arrival_time)
#arrival_time = 1543216500
time = list()
lng = list()
lat = list()
duration = list()
dest = input('Where do you work?')

dest_URL = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s')%(dest,api_key)
dest_URL = wz.url_fix(dest_URL)

dest_json = json.load(ur.urlopen(dest_URL))

if dest_json['status'] == 'ZERO_RESULTS':
    print('Error, destination invald! wtf!')
    quit()
else:
    dest_longlat = dest_json['results'][0]['geometry']['location']
    print(dest_longlat)
#https://en.wikipedia.org/wiki/Geographic_coordinate_system
#Latitude: 1 deg = 110.574 km
#Longitude: 1 deg = 111.320*cos(latitude) km

latdeg_rad = math.radians(dest_longlat['lat'])

lat_degpermeter = 1/(111.543*1000)
lng_degpermeter = 1/(111.320*1000*math.cos(latdeg_rad))
#the *1000 is km -> m. To start i take a 10*10km square around the work destination
latstart = dest_longlat['lat']+10*1000*lat_degpermeter
lngstart = dest_longlat['lng']-10*1000*lng_degpermeter


gmap_URL = 'https://maps.googleapis.com/maps/api/directions/json?mode=transit&'
# The Reihenfolge %s is gmaps_URL, origin, dest, mode, arrival_time, api_key
#How many 500 m are there in 20 km ? -> 20*1000/500 = 40. Also every 500m it saves the long/lat
for i in range(40):
    for j in range(40):
        lat.append(latstart - i*500*lat_degpermeter)
        lng.append(lngstart + j*500*lng_degpermeter)
querynr = 0

for i in range(1600):
    query_url = '%sorigin=%s,%s&destination=%s&arrival_time=%s&key=%s'%(gmap_URL,lat[i],lng[i],dest,arrival_time,api_key)
    query_url = wz.url_fix(query_url)
    result = json.load(ur.urlopen(query_url))
    if result['status'] == 'ZERO_RESULTS':
        time.append(5000)
        print('No times for those coordinates')
        print(query_url)
    else:
        time.append(result['routes'][0]['legs'][0]['duration']['value'])
        print(result['routes'][0]['legs'][0]['duration']['value']/60, "minutes")
    querynr += 1
    print(querynr)
#This is needed if we read it out from a text file:
#time = np.genfromtxt('time.csv',dtype='str',delimiter=',')
print(time, "seconds")
int_time = list()
for i in range(len(time)):
    int_time.append(float(time[i]))
        #This is if we save it into time (a file) and read it out into a list.
        # duration.append(duration_data[square_time].astype(np.float))
        # square_time += 1
cols = ['latitude','longitude','duration']
df = pd.DataFrame(columns = cols)
df['longitude'] = pd.Series(lng)
df['latitude'] = pd.Series(lat)
df['duration'] = pd.Series(int_time)
print(df.head())


gmaps.configure(api_key='AIzaSyDDRjczHB5nH28R7KLRVdepGpCa-fpdxcI')
fig = gmaps.figure(center=list(dest_longlat.values()), zoom_level=8)
heatmap = gmaps.heatmap_layer(df[['latitude', 'longitude']], weights = df['duration'])
fig
