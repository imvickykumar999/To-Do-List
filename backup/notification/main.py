import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

# Fetch tasks from the provided URL and filter only the incomplete ones
def fetch_incomplete_tasks():
    url = 'https://ajaxtodolist.pythonanywhere.com/get_tasks/'
    response = requests.get(url)
    
    if response.status_code == 200:
        tasks = response.json().get('tasks', [])
        incomplete_tasks = [task for task in tasks if not task['is_completed']]
        return incomplete_tasks
    else:
        print(f"Failed to fetch tasks. Status code: {response.status_code}")
        return []

def get_access_token(secret):
    credentials = service_account.Credentials.from_service_account_file(
        secret, scopes=['https://www.googleapis.com/auth/firebase.messaging']
    )
    request = google.auth.transport.requests.Request()
    credentials.refresh(request)
    return credentials.token

def send_push_notification(token, title, body, ProjectID, secret):
    access_token = get_access_token(secret)
    url = f"https://fcm.googleapis.com/v1/projects/{ProjectID}/messages:send"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

if __name__ == "__main__":
    fcm_token = 'cnrKLalKM68kqantC3MC4V:APA91bHlaQ9qdrcQc-RPc7s5OSxn7HB9w00-ZUJ6Ltb4juc9epOzneXSxyBrVZbcSYE_ugW4POj05PL5_uRi3aDyPQFyJ2bgHaRWPnb-7IzQlv5eqIYrdbg6KsU6xnDCc9RO5sr_7_62' # mobile
    
    ProjectID = 'fir-push-notification-85613'
    secret = 'serviceAccountKey.json'
    
    # Fetch only the incomplete tasks
    incomplete_tasks = fetch_incomplete_tasks()
    print('Incomplete Tasks:', incomplete_tasks)
    
    # Send push notification for each incomplete task (if any)
    if incomplete_tasks:
        for first_task in incomplete_tasks:
            title = first_task['name']
            body = 'Task Pending'
            
            response = send_push_notification(fcm_token, title, body, ProjectID, secret)
            print('Response:', response)
    else:
        print("No incomplete tasks found.")
