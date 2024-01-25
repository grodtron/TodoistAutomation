from typing import Optional, List, Dict
import uuid
import requests
from your_data_classes import ConcreteTodoistObjects, ConcreteTodoistLabel, ConcreteTodoistFilter, ConcreteTodoistProject

class TodoistApiWrapper:
    API_URL = "https://api.todoist.com/sync/v9/sync"
    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_all_todoist_objects(self) -> ConcreteTodoistObjects:
        response = self._make_sync_request(sync_token="*", resource_types=["labels", "filters", "projects"])

        labels = [ConcreteTodoistLabel(**label) for label in response.get("labels", [])]
        filters = [ConcreteTodoistFilter(**filter_) for filter_ in response.get("filters", [])]
        projects = [ConcreteTodoistProject(**project) for project in response.get("projects", [])]
        
        return ConcreteTodoistObjects(labels=labels, filters=filters, projects=projects)

    def update_todoist_objects(self, todoist_objects: ConcreteTodoistObjects) -> None:
        sync_commands = []

        for item in todoist_objects.get_all_items():
            item_type = item.get_type()
            sync_commands.append(self._create_update_command(item_type, item.id, item))

        self._make_batched_sync_request(sync_commands)


    def _create_update_command(self, item_type: str, item_id: Optional[int], updated_item) -> Dict:
        action_type = "update" if item_id else "add"
        command = {
            "type": f"{item_type}_{action_type}",
            "uuid": str(uuid.uuid4()),
            "args": {"id": item_id} if item_id else {"temp_id": str(uuid.uuid4())},
            **updated_item.as_dict(),
        }
        return command

    def _make_sync_request(self, sync_token: str, resource_types: Optional[List[str]] = None) -> Dict:
        payload = {
            "token": self.api_key,
            "sync_token": sync_token,
            "resource_types": resource_types,
        }
        response = requests.post(self.API_URL, headers=self.HEADERS, data=payload)
        return response.json()

    def _make_batched_sync_request(self, sync_commands: List[Dict]) -> Dict:
        batched_payload = {"commands": sync_commands}
        response = requests.post(self.API_URL, headers=self.HEADERS, json=batched_payload)
        return response.json()
