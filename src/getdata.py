import requests

useragent = "Python"
headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '"Google Chrome 80"',
    "Accept": "*/*",
    "Sec-Fetch-Dest": "empty",
    "User-Agent": useragent,
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://overpass-turbo.eu",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Referer": "https://overpass-turbo.eu/",
    "Accept-Language": "",
    "dnt": "1",
}


def main(config):

    config = config["download"]

    query = f"""
        way({config["min_lat"]},{config["min_lon"]},{config["max_lat"]},{config["max_lon"]}) ["highway"];
        (._;>;);
        out body;
        """

    data = {"data": query}

    response = requests.post(
        "https://overpass-api.de/api/interpreter", headers=headers, data=data
    )

    with open(config["output_filename_xml"], "w") as f:
        f.write(response.text)


if __name__ == "__main__":
    main()
