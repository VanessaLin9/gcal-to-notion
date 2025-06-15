import datetime
import os
import sys
import requests
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load Notion secrets
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Token paths
TOKEN_PATH = os.path.join(BASE_DIR, 'token.json')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials.json')

# Google Calendar API Scope
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

DATE_AHEAD = 14  # Check for events in the next 14 days
force_login = '--force-login' in sys.argv

def get_upcoming_events(check_range):
    creds = get_credentials() 
    # if os.path.exists(TOKEN_PATH):
    #     creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    # else:
    #     flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    #     creds = flow.run_console()
    #     # Save the credentials for the next run
    #     with open(TOKEN_PATH, 'w') as token:
    #         token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow()
    future = now + datetime.timedelta(days=check_range)
    events_result = service.events().list(
        calendarId='primary', 
        timeMin=now.isoformat() + 'Z',
        timeMax=future.isoformat() + 'Z',
        maxResults=100, 
        singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
        return None
    return events


def get_credentials():
    if force_login or not os.path.exists(TOKEN_PATH):
        print("Login Google on the browser!")
        flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
        creds = flow.run_local_server(port=0, open_browser=True)  # 自動打開預設瀏覽器
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
        print("✅ Login successful and token saved.")
    else:
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return creds


def check_event_exists(event_id):
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "filter": {
            "property": "event_id",
            "rich_text": {
                "equals": event_id
            }
        }
    }
    res = requests.post(url, headers=headers, json=data)
    return res.status_code == 200 and len(res.json().get('results', [])) > 0

def create_notion_item(event):
    title = event['summary']
    start_time = event['start'].get('dateTime', event['start'].get('date'))
    end_time = event['end'].get('dateTime', event['end'].get('date'))

    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    data = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "任務名稱": {
                "title": [{ "text": { "content": title } }]
            },
            "執行時間": {
                "date": { "start": start_time, "end": end_time }
            },
            "清單":{
                "select": { "name": "Google Calendar" }
            },
            "event_id": {
                "rich_text": [{ "text": { "content": event['id'] } }]
            }
        }
    }

    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 200 or res.status_code == 201:
        print("✅ Event added to Notion!")
    else:
        print("❌ Failed to add to Notion:", res.text)

# Main execution
if __name__ == '__main__':
    results = []
    event = get_upcoming_events(DATE_AHEAD)
    if not event:
        results.append("No events found in the next 14 days.")
    else:
        for event in event:
            if not check_event_exists(event['id']):
                results.append(f"✅ Event does not exist in Notion: {event['summary']}")
                create_notion_item(event)
            else:
                results.append(f"❌ Event already exists in Notion: {event['summary']}")
    
    print("\n".join(results))

