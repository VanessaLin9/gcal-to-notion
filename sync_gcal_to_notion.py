import datetime
import os
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

# Google Calendar API Scope
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

DATE_AHEAD = 14  # Check for events in the next 14 days

def get_upcoming_events(check_range):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(BASE_DIR, 'credentials.json'), SCOPES
        )
        creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

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

if __name__ == '__main__':
    event = get_upcoming_events(DATE_AHEAD)
    if not event:
        print("No events found in the next 14 days.")
        exit(0)
    else:
        for event in event:
            if not check_event_exists(event['id']):
                print(f"✅ Event does not exist in Notion: {event['summary']}")
                create_notion_item(event)
            else:
                # If the event already exists in Notion, skip it
                print(f"❌ Event already exists in Notion: {event['summary']}")
