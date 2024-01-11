# this script uses the overpass api (openstreetmap) to get updated fountain data

import requests
import json
import os

AREA_LIST = [
    ("CH", "Switzerland"),
    ("DE", "Germany"),
    ("FR", "France"),
    ("IT", "Italy"),
    ("AT", "Austria"),
    ("LI", "Liechtenstein"),
]

# create a new directory called exports if it doesn't exist
if not os.path.exists("exports"):
    os.makedirs("exports")


query_template = """
[out:json][timeout:25];
area["ISO3166-1"="{}"][admin_level=2];
node["amenity"="drinking_water"](area);
node["amenity"="fountain"](area);
out center;
"""

# loop through all the areas
for area in AREA_LIST:
    # get the area code and the area name
    area_code, area_name = area
    # create a new query using the template and the area code
    query = query_template.format(area_code)
    # send the query to the overpass api
    response = requests.get("http://overpass-api.de/api/interpreter", params={"data": query})
    # check if the response was successful
    if response.status_code != 200:
        # the response was not successful
        print("Error: Could not get data from overpass api")
        exit()

    # restructure the response to be a geojson
    response = response.json()

    # rearrange the response to be a geojson
    response = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": node["tags"],
                "geometry": {
                    "type": "Point",
                    "coordinates": [node["lon"], node["lat"]]
                }
            } for node in response["elements"]
        ]
    }
    # minify the response
    response = json.dumps(response, separators=(',', ':'))
    # write the response to a file
    with open("exports/{}.geojson".format(area_name), 'w') as f:
        f.write(response)
    print("Wrote response to file: {}.geojson".format(area_name))