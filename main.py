import requests, json
from bs4 import BeautifulSoup as bs
from progress.bar import Bar

TARGET = "https://onlineradiobox.com/id/"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

file_name = "indonesian_radio"

def get_total_page():
    pageResponse = requests.get(TARGET, headers=HEADERS)

    if pageResponse.status_code != 200:
        print(f"status: {pageResponse.status_code}")
        print(f"failed to load firstpage!")
    
    soup = bs(pageResponse.content, 'html.parser')

    paginationItem = soup.select("dl.pagination dd")
    lastPage = paginationItem[len(paginationItem)-3]
    lastPageIndex = int(lastPage.select_one("a").text) - 1
    return lastPageIndex


def get_content_per_page(index = 0):
    pageResponse = requests.get(f"{TARGET}?p={index}", headers=HEADERS)

    if pageResponse.status_code != 200:
        print(f"status: {pageResponse.status_code}")
        print(f"failed to load page at index: {index}!")
    
    
    soup = bs(pageResponse.content, 'html.parser')

    stationList = soup.select(".stations-list .stations__station")

    stations = []

    for station in stationList:
        button = station.select_one("button.station_play")
        stations.append({
            "radio_id": button['radioid'],
            "radio_name": button['radioname'],
            "radio_img": f"https:{button['radioimg']}",
            "stream_url": button['stream'],
            "stream_type": button['streamtype']
        })

    return stations


def to_json(data):
    json_result = json.dumps(data, indent=4)

    with open(file_name + ".json", "w") as json_file:
        json_file.write(json_result)


totalPage = get_total_page()

allStations = []

bar = Bar("Fetching data: ", max=int(totalPage+1))

for pageIndex in range(totalPage+1):
    stations = get_content_per_page(pageIndex)
    allStations = allStations + stations
    bar.next()

bar.finish()

to_json(allStations)