import os

import requests
import json


def current_wait_times():
    url = "https://www.tapingo.com/mobile/"

    querystring = {"v": "2"}

    payload = "{\"user_info\":\"\",\"shop_list\":{\"location\":{\"longitude\":-75.1106483,\"latitude\":39.7065334}}}"
    headers = {
        'cookie': "sessionid=" + os.environ['TAPINGO_SESSION_ID']
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    j = json.loads(response.text)

    data = []
    for shopId in j["shops"]:
        shop = j["shops"][shopId]
        if ("lassboro" in shop["address_str"] and "eal" not in shop["name"]):
            name = shop["name"]

            # Workaround for Brkfst & Co.
            name = name.replace("Brkfst", "Breakfast")

            status = "Coming Soon" if shop["coming_soon"] else "Open" if shop["is_open"] else "Closed"
            eta = "-" if not shop["is_open"] or shop["coming_soon"] else shop["service_info"][0]["eta"]
            line = "-" if not shop["is_open"] or shop["coming_soon"] else str(shop["people_in_line"])
            data.append([name, status, eta, line])

    data.sort()

    #data.insert(0, ["NAME", "STATUS", "ETA", "LINE"])
    widths = [max(map(len, col)) for col in zip(*data)]
    for row in data:
        print("  ".join((val.ljust(width) for val, width in zip(row, widths))))

    return data
