import requests
import json
import time

# SLACK
SLACK_WEBHOOK_URL = '' # UPDATE URL
SLACK_CHANNEL = '#mbta'
SLACK_BOT_NAME = 'MBTA ALERT'
SLACK_BOT_IMAGE = ''

# MBTA 
MBTA_API_KEY = '' # UPDATE KEY
MBTA_URL = 'http://realtime.mbta.com/developer/api/v2/'
MBTA_REQUEST_TYPE = 'alertheadersbyroute'
MBTA_ACCESS_ALERTS = 'false'
MBTA_SERVICE_ALERTS = 'true'
FORMAT = 'json'

alert_ids = []

# CUSTOM IMAGE FOR EACH LINE
orange_line = 'http://i.imgur.com/emzpdue.jpg'
red_line = 'http://i.imgur.com/nYplkpw.png'
green_line = 'http://i.imgur.com/gtEpbEm.png'
blue_line = 'http://i.imgur.com/u3VO5jt.jpg'
silver_line = 'http://i.imgur.com/IzGUM4H.jpg'

routes = ['orange', 'red', 'silver', 'green', 'blue']

polling_interval = 120.0

running = True

def mbta():
    
    for route in routes:
        
        requestURL = MBTA_URL + MBTA_REQUEST_TYPE + \
        '?api_key=' + MBTA_API_KEY + \
        '&include_access_alerts=' + MBTA_ACCESS_ALERTS + \
        '&include_service_alerts=' + MBTA_SERVICE_ALERTS + \
        '&format=' + FORMAT + \
        '&route=' + route

        mbtaRequest = requests.get(requestURL)
        mbtaResponse = mbtaRequest.json()

        if 'alert_headers' in mbtaResponse:
            
            for item in mbtaResponse['alert_headers']:

                aid = item.get("alert_id")
                int(aid)
                text = item.get("header_text")
                
                if aid not in alert_ids:
                    alert_ids.append(aid)
                    slack(aid, route, text)

def slack(aid, route, text):

    if route == 'orange':
        SLACK_BOT_IMAGE = orange_line
        SLACK_BOT_NAME = 'MBTA ALERT (ORANGE LINE)'
    if route == 'red': 
        SLACK_BOT_IMAGE = red_line
        SLACK_BOT_NAME = 'MBTA ALERT (RED LINE)'
    if route == 'green': 
        SLACK_BOT_IMAGE = green_line
        SLACK_BOT_NAME = 'MBTA ALERT (GREEN LINE)'
    if route == 'silver': 
        SLACK_BOT_IMAGE = silver_line
        SLACK_BOT_NAME = 'MBTA ALERT (SILVER LINE)'
    if route == 'blue': 
        SLACK_BOT_IMAGE = blue_line
        SLACK_BOT_NAME = 'MBTA ALERT (BLUE LINE)'

    payload = {'channel': SLACK_CHANNEL, 'username': SLACK_BOT_NAME, 'text': text, 'icon_url': SLACK_BOT_IMAGE}
    
    slackPost = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))

while running:
    
    start = time.clock()
    mbta()
    work_duration = time.clock() - start
    time.sleep(polling_interval - work_duration)