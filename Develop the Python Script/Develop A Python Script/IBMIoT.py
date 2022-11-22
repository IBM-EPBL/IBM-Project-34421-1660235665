import sys

import ibmiotf.application
import ibmiotf.device
import ibmiotf.application
from geopy.geocoders import Nominatim
import time
import random




organization = "srpvqy"
deviceType = "Bin_Monitoring"
deviceId = "Bin_1"
authMethod= "token"
authToken = "(Z+UCAjRQvT)*@px)5"


def myCommandCallback(cmd):
    print("command received: %s" % cmd.data['command'])

    status = cmd.data['command']

    if status=="lighton":
        print("Led is on")
    else:
        print("Led is off")

try:
    deviceOptions={"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
    deviceCli=ibmiotf.device.Client(deviceOptions)
except Exception as e:
    print("caught exception connecting device %s" %str(e))
    sys.exit()

deviceCli.connect()

while True:

    level = random.randint(0, 100)

    weight = level*2.5

    ladegree = 12.0
    lodegree = 79.0

    laminute = random.randint(0, 60)
    lominute = random.randint(0, 60)

    lasecond = random.uniform(0, 3600)
    losecond = random.uniform(0, 3600)

    latitude = (round(((ladegree) + (laminute / 60) + (lasecond / 3600)), 14))
    longitude = (round(((lodegree) + (lominute / 60) + (losecond / 3600)), 14))

    if longitude > 80.33 or latitude > 13.39:
        continue
    else:

        geolocator = Nominatim(user_agent="MyApp")

        coordinates = str(latitude) + ", " + str(longitude)

        location = geolocator.reverse(coordinates)

        address = location.raw['address']

        city = address.get('city', '')
        state = address.get('state', '')
        country = address.get('country', '')
        town = address.get('town', '')
        village = address.get('village', '')
        municipality = address.get('municipality', '')
        suburb = address.get('suburb', '')
        county = address.get('county', '')

        l = [city, suburb, town, municipality, county, village]

        l = sorted(l, key=lambda x: (len(x)), reverse=True)

        fp = l[0]
        fs = state
        fc = country

    if len(fp) != 0 and len(fs) != 0 and len(fc) != 0:
        print(fp, fs, fc, sep="\n")
        data = {'level': level,'weight': weight,'coordinates': coordinates, 'city': fp, 'state': fs, 'country': fc}
        def myOnPublishCallback():
            print("published Level = %d " % level,"Weight = %d " % weight, "Coordinates = %s " % coordinates, "City = %s " % fp, "State = %s " % fs, "Country = %s " %fc)
            # print("Published")
        success = deviceCli.publishEvent("IoTSensor", "json", data, qos=0, on_publish=myOnPublishCallback())
        if not success:
            print("not connected to ibmiot")
            level=0
    if level>80:
        time.sleep(30)
    else:
        time.sleep(1)
    deviceCli.commandCallback = myCommandCallback
deviceCli.disconnect()