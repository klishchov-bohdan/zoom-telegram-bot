import base64

import requests
from data import config


def get_access_token():
    try:
        creds_str = f'{config.ZOOM_CLIENT_ID}:{config.ZOOM_CLIENT_SECRET}'
        creds_base64_bytes = base64.b64encode(creds_str.encode('ascii'))
        base64_creds = creds_base64_bytes.decode('ascii')

        headers = {
            'Host': 'zoom.us',
            'Authorization': f'Basic {base64_creds}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'grant_type': 'account_credentials',
            'account_id': f'{config.ZOOM_ACCOUNT_ID}',
        }

        proxies = {
           'https': 'http://l1mb0:bogdan2525_country-ua_streaming-1@geo.iproyal.com:12321',
        }
        response = requests.post('https://zoom.us/oauth/token', headers=headers, data=data, proxies=proxies)
        if response.status_code == 200:
            resp_json = response.json()
            return resp_json['access_token']
    except Exception as ex:
        print(ex)


def start_zoom_meeting(access_token):
    try:
        headers = {
            'Host': 'api.zoom.us',
            'Authorization': f"Bearer {access_token}",
        }
        print(headers)

        json_data = {
          "agenda": "My Meeting",
          "duration": 40,
          "password": "123456",
          "settings": {
            "host_video": True,
            "participant_video": True,
            "join_before_host": True,
            "mute_upon_entry": True,
            "breakout_room": {
              "enable": True,
            },
          },
          "start_time": "2022-03-25T07:32:55Z",
          "timezone": "America/Los_Angeles",
          "topic": "My Meeting",
          "type": 2
        }
        proxies = {
            'https': 'http://l1mb0:bogdan2525_country-ua_streaming-1@geo.iproyal.com:12321',
        }
        response = requests.post('https://api.zoom.us/v2/users/me/meetings', headers=headers, json=json_data, proxies=proxies)
        if response.status_code == 201:
            return response.json()
    except Exception as ex:
        print(ex)
