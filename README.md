# indonesian-radio-scraper

Scraper for fetching all Indonesian radio stations from onlineradiobox.com and export the result as JSON file

## How to use?
### Install dependencies
```
pip3 install -r requirements.txt
```

### Run the project
```
python3 main.py
```
### Output
```
// filename: indonesian_radio.json
[
  {
    "radio_id": "...",
    "radio_name": "...",
    "radio_img": "...",
    "stream_url": "...",
    "stream_type": ..." // mp3 or m3u8
  },
  ... 
  // another station object
]
```
