#!/usr/bin/python3

from dataclasses import dataclass
import json
import requests
import uuid



@dataclass
class GTDContextLabel:
    name: str
    emojis: str
    color: str

    def generate_title(self):
        # Combine emojis and name in title case
        title = f"{self.emojis} {self.name.title()}"
        return title

    def generate_filter(self):
        # Generate Todoist filter for the label or project
        filter_query = f"#{self.name}{' ' * 40}| (@{self.name} & !#NotNow)"
        return filter_query


def create_filter_add_request(name, query, color):
    temp_id = str(uuid.uuid4())
    filter_uuid = str(uuid.uuid4())

    request_json = {
        "type": "filter_add",
        "temp_id": temp_id,
        "uuid": filter_uuid,
        "args": {
            "name": name,
            "query": query,
            "is_favorite": True,
            "color": color
        }
    }
    return request_json



contexts = map(lambda t: GTDContextLabel(*t), [
    ("home", "🏠🧺🧹🛠️", "orange"),
    ("yard", "🏡🌳🍃", "lime_green"),
    ("errand", "🚴💼🎒🛍️", "red"),
    ("call", "📞🗣️📲", "mint_green"),
    ("iphone", "✨ 🤳 👀", "yellow"),
    ("computer", "📝📊📑", "sky_blue"),
    ("schedule", "🗓️🧱⏰⏲️", "berry_red"),
    ("focused", "🎧🧠💻", "charcoal"),
    ("quick", "⚡️💻✨", "charcoal"),
])


filter_add_requests = [
    create_filter_add_request(label.generate_title(), label.generate_filter(), label.color)
    for label in contexts
]

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

api_token = "EDIT THIS TO ADD YOUR API TOKEN"


response = send_todoist_sync_request(api_token, filter_add_requests)

if response:
    print(response)

