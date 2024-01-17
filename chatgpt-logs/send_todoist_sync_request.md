# Todoist API Request Function

## You
Here is documentation on the Todoist v9 sync API.


Example add filter request:
$ curl https://api.todoist.com/sync/v9/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "filter_add", 
        "temp_id": "9204ca9f-e91c-436b-b408-ea02b3972686", 
        "uuid": "0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8", 
        "args": {
            "name": "Important", 
            "query": "priority 1"
        }
    }]'
Example response:
{
  ...
  "sync_status": {"0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8": "ok"},
  "temp_id_mapping": {"9204ca9f-e91c-436b-b408-ea02b3972686": "4638878"},
  ...
}

suppose I have a list of python dictionaries representing the "commands" objects. Can you write me a function that would construct the request and send it?

## ChatGPT
Certainly! You can use the `requests` library in Python to send HTTP requests. Below is a simple function that takes a list of command dictionaries and sends the corresponding request to the Todoist v9 sync API:

```python
import requests
import json

def send_todoist_sync_request(api_token, commands):
    url = "https://api.todoist.com/sync/v9/sync"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "commands": commands
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage:
api_token = "0123456789abcdef0123456789abcdef01234567"

commands = [
    {
        "type": "filter_add",
        "temp_id": "9204ca9f-e91c-436b-b408-ea02b3972686",
        "uuid": "0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8",
        "args": {
            "name": "Important",
            "query": "priority 1"
        }
    }
]

response = send_todoist_sync_request(api_token, commands)

if response:
    print(response)

```

Make sure to replace the `api_token` with your actual Todoist API token, and adjust the `commands` list based on your requirements. This example assumes that the Todoist API token is provided as a string and the commands list is a list of dictionaries. The function returns the parsed JSON response from the API or `None` if an error occurs.

