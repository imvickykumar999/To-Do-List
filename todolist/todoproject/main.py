import json
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

# Function to log in using username and password with CSRF token handling
def login(username, password):
    login_url = 'https://ajaxtodolist.pythonanywhere.com/login/'  # Replace with your login endpoint
    session = requests.Session()  # Create a new session to persist login state

    # Get the CSRF token by making a GET request to the login page
    try:
        get_response = session.get(login_url)
        # Extract the CSRF token from the cookies
        csrftoken = get_response.cookies.get('csrftoken')

        if not csrftoken:
            print("Failed to retrieve CSRF token.")
            return None

        # Prepare login data with CSRF token included
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrftoken
        }

        # Include the CSRF token in the headers
        headers = {
            'Referer': login_url,
            'X-CSRFToken': csrftoken
        }

        # Post the username and password to the login endpoint
        response = session.post(login_url, data=login_data, headers=headers)
        if response.status_code == 200:
            print("Login successful.")
            return session  # Return the logged-in session
        else:
            print(f"Login failed with status code {response.status_code}. Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during login: {e}")
        return None

# Fetch tasks from the provided URL and filter only the incomplete ones using session-based authentication
def fetch_incomplete_tasks(session):
    url = 'https://ajaxtodolist.pythonanywhere.com/get_tasks/'
    try:
        # Use the session to make a GET request to the task endpoint
        response = session.get(url)
        if response.status_code == 200:
            tasks = response.json().get('tasks', [])
            incomplete_tasks = [task for task in tasks if not task['is_completed']]
            return incomplete_tasks
        elif response.status_code == 403 or response.status_code == 401:
            print("Authorization error: Please check your credentials or session settings.")
        elif response.status_code == 404:
            print(f"Failed to fetch tasks. The endpoint {url} was not found (404). Please check the URL or server settings.")
        else:
            print(f"Failed to fetch tasks. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return []

# Retrieve the Firebase Cloud Messaging access token using the service account file
def get_access_token(secret):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            secret, scopes=['https://www.googleapis.com/auth/firebase.messaging']
        )
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        return credentials.token
    except Exception as e:
        print(f"Failed to get access token: {e}")
        return None

# Send push notification using Firebase Cloud Messaging
def send_push_notification(token, title, body, ProjectID, secret):
    access_token = get_access_token(secret)
    if not access_token:
        print("Failed to get access token. Push notification aborted.")
        return

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

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("Push notification sent successfully.")
        else:
            print(f"Failed to send push notification. Status code: {response.status_code}, Response: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the push notification: {e}")
    return response.json()

if __name__ == "__main__":
    # Replace these with your Firebase Cloud Messaging (FCM) token and Google Cloud Project ID
    fcm_token = 'cnrKLalKM68kqantC3MC4V:APA91bHlaQ9qdrcQc-RPc7s5OSxn7HB9w00-ZUJ6Ltb4juc9epOzneXSxyBrVZbcSYE_ugW4POj05PL5_uRi3aDyPQFyJ2bgHaRWPnb-7IzQlv5eqIYrdbg6KsU6xnDCc9RO5sr_7_62'
    ProjectID = 'fir-push-notification-85613'
    secret = 'serviceAccountKey.json'  # Path to your service account key file

    # Login using username and password
    username = '1'  # Replace with your username
    password = '1'  # Replace with your password

    # Authenticate and get a session
    session = login(username, password)
    if not session:
        print("Exiting due to failed login.")
    else:
        # Fetch only the incomplete tasks using the authenticated session
        incomplete_tasks = fetch_incomplete_tasks(session)
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
