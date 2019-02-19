from urllib import parse, request
import json

# API key
api_key = 'c5fb2941-a56f-4472-b3ae-a21c9018f005'

# Adres
adres = 'Mr van Rhemenslaan'
huisnummer = 3
postcode = '7316AJ'
stad = 'Apeldoorn'

# URLLib data
url = 'https://geodata.nationaalgeoregister.nl/locatieserver/v3/suggest?q=' + parse.quote_plus( adres + " " +
                             str(huisnummer) + " " + postcode)
hdr = {'X-Api-Key': api_key}

req = request.Request(url, headers=hdr)
response = request.urlopen(req)
response_json = json.loads(response.read())

address_id = response_json['response']['docs'][0]['id']

url2 = 'https://geodata.nationaalgeoregister.nl/locatieserver/v3/lookup?id=' + parse.quote_plus(address_id)
req2 = request.Request(url2, headers=hdr)
response2 = request.urlopen(req2)
response_json2 = json.loads(response2.read())
centroide_string = response_json2['response']['docs'][0]['centroide_ll']
centroide_array = [float(centroide_string.split('(')[1].split(' ')[0]),
                   float(centroide_string.split('(')[1].split(' ')[1].split(')')[0])]
print(centroide_array)
post_dict = {
    "geometrie": {
        "contains": {
            "type": "Point",
            "coordinates": centroide_array
        }
    }
}
url3 = "https://bag.basisregistraties.overheid.nl/api/v1/panden"
data = json.dumps(post_dict).encode('utf8')
req3 = request.Request(url3, data=data, headers=hdr)
response3 = request.urlopen(req3)
response_json3 = json.loads(response3.read())
print(response_json3)

url4 = response_json3['_embedded']['panden'][0]['_links']['verblijfsobjecten']['href']
req4 = request.Request(url4, headers=hdr)
response4 = request.urlopen(req4)
response_json4 = json.loads(response4.read())
print(response_json4['_embedded']['verblijfsobjecten'][0]['oppervlakte'])
