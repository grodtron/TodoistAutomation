import logging
import uuid
import requests
from autodoist.models import (
    ConcreteTodoistObjects,
    ConcreteTodoistLabel,
    ConcreteTodoistFilter,
    ConcreteTodoistProject,
)

class TodoistAPIRequester:
    API_URL = "https://api.todoist.com/sync/v9/sync"
    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def make_request(self, **payload) -> Dict:
        self.logger.debug(f"Sending request to {self.API_URL} with payload: {payload}")
        response = requests.post(self.API_URL, headers=self.HEADERS, data=payload)
        self.logger.debug(f"Received response: {response.content}")
        return response.json()

class TodoistApiWrapper:
    def __init__(self, api_requester: TodoistAPIRequester):
        self.api_requester = api_requester
        self.logger = logging.getLogger(__name__)

    def get_all_todoist_objects(self) -> ConcreteTodoistObjects:
        response = self.api_requester.make_request(
            sync_token="*", resource_types=["labels", "filters", "projects"]
        )
        self.logger.debug(f"Received Todoist objects: {response}")
        labels = [ConcreteTodoistLabel(**label) for label in response.get("labels", [])]
        filters = [
            ConcreteTodoistFilter(**filter_) for filter_ in response.get("filters", [])
        ]
        projects = [
            ConcreteTodoistProject(**project)
            for project in response.get("projects", [])
        ]

        return ConcreteTodoistObjects(labels=labels, filters=filters, projects=projects)

    def update_todoist_objects(self, todoist_objects: ConcreteTodoistObjects) -> Dict:
        sync_commands = []

        for item in todoist_objects.get_all_items():
            item_type = item.get_type()
            sync_commands.append(self._create_update_command(item_type, item.id, item))
        
        self.logger.debug(f"Sending update commands: {sync_commands}")
        return self.api_requester.make_request(commands=sync_commands)

    def _create_update_command(
        self, item_type: str, item_id: Optional[int], updated_item
    ) -> Dict:
        action_type = "update" if item_id else "add"
        command = {
            "type": f"{item_type}_{action_type}",
            "uuid": str(uuid.uuid4()),
            "args": updated_item.to_dict(),
        }

        if item_id:
            command["args"]["id"] = item_id
        else:
            command["temp_id"] = str(uuid.uuid4())

        return command

class DryRunTodoistApiWrapper(TodoistApiWrapper):
    def update_todoist_objects(self, todoist_objects: ConcreteTodoistObjects) -> Dict:
        sync_commands = []

        for item in todoist_objects.get_all_items():
            item_type = item.get_type()
            command = self._create_update_command(item_type, item.id, item)
            sync_commands.append(command)
            self.logger.debug(f"Dry run command: {command}")

        self.logger.info("Dry run completed. No changes were made.")
        return dict()
