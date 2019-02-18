from pyPostcode import Api
from math import radians, cos, sin, asin, sqrt
import urllib.request
import json
import sys

global bingApiKey
bingApiKey = "Ajh2QYJKvUUVGSFYO6OvyxQgpf-o10BEnNgG6PeoQNz8jDhnUzNaKmJk4PiI6zAi"

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def getLocation(landCode, postcodeLetters, postcodeNumbers, city,housenumber):
	contents = urllib.request.urlopen("http://dev.virtualearth.net/REST/v1/Locations/"+landCode+"/"+postcodeLetters+"/"+postcodeNumbers+"/"+housenumber+"/"+city+"%20Microsoft%20Way?o=json&key=Ajh2QYJKvUUVGSFYO6OvyxQgpf-o10BEnNgG6PeoQNz8jDhnUzNaKmJk4PiI6zAi").read()
	return contents

def getLocationForWeatherStation(landCode, city):
	contents = urllib.request.urlopen("http://dev.virtualearth.net/REST/v1/Locations/"+landCode+"/"+city+"%20Microsoft%20Way?o=json&key=Ajh2QYJKvUUVGSFYO6OvyxQgpf-o10BEnNgG6PeoQNz8jDhnUzNaKmJk4PiI6zAi").read()
	return contents

def getCoordinates(locationData,city):
	for resource in locationData["resourceSets"][0]["resources"]:
		if city.lower() in resource["name"].lower():
			return resource["point"]["coordinates"]

def getWeatherStations(path):
	if path:
		with open(path, 'r') as f:
			datastore = json.load(f)
	return datastore

def findClosestWeatherstation(coordinates,weatherstations):
	smallestValue = 99999999
	nameOfWeatherstation = ""
	for weatherstation in weatherstations:
		city = weatherstation["NAME"].lower()
		coordinates2 = getCoordinates(json.loads(getLocationForWeatherStation("NL",city.replace(" ","%20"))),city)
		# print("\n")
		# print(city,haversine(coordinates[0],coordinates[1],coordinates2[0],coordinates2[1]))
		if haversine(coordinates[0],coordinates[1],coordinates2[0],coordinates2[1]) < smallestValue:
			smallestValue = haversine(coordinates[0],coordinates[1],coordinates2[0],coordinates2[1])
			nameOfWeatherstation = weatherstation["STN"]
	return nameOfWeatherstation, smallestValue

def getWeatherData(path):
	if path:
		with open(path, 'r') as f:
			datastore = json.load(f)
	return datastore

def getWeatherOnDateOnStation(weatherdata,date,nameOfStation):
	for weatherdataOnDate in weatherdata:
		if weatherdataOnDate["STN"] == nameOfStation:
			if weatherdataOnDate["YYYYMMDD"] == date:
				return weatherdataOnDate



coordinates = getCoordinates(json.loads(getLocation("NL","AJ","7316","Apeldoorn","3")),"Apeldoorn")

weatherstations = getWeatherStations("weatherstations.json")
nameOfStation, distance = findClosestWeatherstation(coordinates,weatherstations)
print("Closest station is ",nameOfStation, "Distance to location is: ", distance, "KM")
weatherdata = getWeatherData("weatherdata.json")
if len(sys.argv) <2:
	print("No date given please give date in YYYYMMDD format")
else:
	dateOfWeather = int(sys.argv[1])
	weather = getWeatherOnDateOnStation(weatherdata,dateOfWeather,int(nameOfStation))
	print(weather)