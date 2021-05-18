import geoip2.database
from pprint import pprint

reader = geoip2.database.Reader('Geo/GeoLite2-City.mmdb')

IPV4 = '190.11.0.167'

response = reader.city(IPV4)

print("response.country.name: {}".format(response.country.name))
print("response.country.iso_code: {}".format(response.country.iso_code))
print("response.subdivisions.most_specific.name: {}".format(response.subdivisions.most_specific.name))
print("response.subdivisions.most_specific.iso_code: {}".format(response.subdivisions.most_specific.iso_code))
print("response.city.name: {}".format(response.city.name))
print("response.city.code: {}".format(response.postal.code))
print("response.location.latitude: {}".format(response.location.latitude))
print("response.location.longitude: {}".format(response.location.longitude))
print("response.traits.connection_type: {}".format(response.traits.connection_type))




input("Press enter to exit ;)")