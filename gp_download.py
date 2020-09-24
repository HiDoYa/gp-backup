from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests

flow = InstalledAppFlow.from_client_secrets_file(
    'gcloud_gp_backups.json',
    scopes=['https://www.googleapis.com/auth/photoslibrary'])

credentials = flow.run_local_server(host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)

gp = build('photoslibrary', 'v1', credentials=credentials)
pageToken = 'temp'

while pageToken != '':
    pageToken = '' if pageToken == 'temp' else pageToken
    res = gp.mediaItems().list(pageSize=100, pageToken=pageToken).execute()
    for item in res['mediaItems']:
        mediaName = item['filename']
        mimeType = item['mimeType']
        mediaUrl = item['baseUrl']

        if 'video' in mimeType:
            mediaUrl += "=dv"
        elif 'image' in mimeType:
            mediaUrl += "=d"
        else:
            print("Unknown mime type found: " + mimeType)
            print(item + '\n')
            continue

        mediaGlob = requests.get(mediaUrl)

        f = open('downloads/' + mediaName, "wb")
        f.write(mediaGlob.content)
        f.close()
    pageToken = res.get('nextPageToken', '')


