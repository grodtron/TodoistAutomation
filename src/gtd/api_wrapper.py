from typing import Optional, List, Dict
import uuid
import requests
from your_data_classes import ConcreteTodoistObjects, ConcreteTodoistLabel, ConcreteTodoistFilter, ConcreteTodoistProject

class TodoistAPIRequester:
    API_URL = "https://api.todoist.com/sync/v9/sync"
    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def make_request(self, **payload) -> Dict:
        response = requests.post(self.API_URL, headers=self.HEADERS, data=payload)
        return response.json()


class TodoistApiWrapper:
    def __init__(self, api_requester: TodoistAPIRequester):
        self.api_requester = api_requester

    def get_all_todoist_objects(self) -> ConcreteTodoistObjects:
        response = self.api_requester.make_request(sync_token="*", resource_types=["labels", "filters", "projects"])
        
        labels = [ConcreteTodoistLabel(**label) for label in response.get("labels", [])]
        filters = [ConcreteTodoistFilter(**filter_) for filter_ in response.get("filters", [])]
        projects = [ConcreteTodoistProject(**project) for project in response.get("projects", [])]
        
        return ConcreteTodoistObjects(labels=labels, filters=filters, projects=projects)

    def update_todoist_objects(self, todoist_objects: ConcreteTodoistObjects) -> None:
        sync_commands = []

        for item in todoist_objects.get_all_items():
            item_type = item.get_type()
            sync_commands.append(self._create_update_command(item_type, item.id, item))

        return self.api_requester.make_request(commands=sync_commands)

    def _create_update_command(self, item_type: str, item_id: Optional[int], updated_item) -> Dict:
        action_type = "update" if item_id else "add"
        command = {
            "type": f"{item_type}_{action_type}",
            "uuid": str(uuid.uuid4()),
            "args": {"id": item_id} if item_id else {"temp_id": str(uuid.uuid4())},
            **updated_item.as_dict(),
        }
        return command
