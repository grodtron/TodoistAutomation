from typing import Optional, List, Dict
import logging
import uuid
import requests
from autodoist.models import (
    ConcreteTodoistObjects,
    ConcreteTodoistLabel,
    ConcreteTodoistFilter,
    ConcreteTodoistProject,
)


import logging
import requests
from typing import Dict


class TodoistAPIRequester:
    API_URL = "https://api.todoist.com/sync/v9/sync"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)

    def make_request(self, **payload) -> Dict:
        self.logger.debug(f"Sending request to {self.API_URL} with payload: {payload}")
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(self.API_URL, headers=headers, data=payload)
        self.logger.debug(f"Received response: {response.content.decode('utf-8')}")

        print(response.status_code)
        print(repr(response))

        if response.status_code != 200:
            self.logger.error(
                f"Request failed with status code: {response.status_code}"
            )
            try:
                error_data = response.json()
                error_message = error_data.get("error", "Unknown error")
                error_code = error_data.get("error_code")
                raise Exception(f"Request failed: {error_message} ({error_code})")
            except ValueError:
                raise Exception("Request failed with unknown error")

        return response.json()


class TodoistApiWrapper:
    def __init__(self, api_requester: TodoistAPIRequester):
        self.api_requester = api_requester
        self.logger = logging.getLogger(__name__)

    def get_all_todoist_objects(self) -> ConcreteTodoistObjects:
        response = self.api_requester.make_request(
            sync_token="*", resource_types='["labels", "filters", "projects"]'
        )
        self.logger.debug(f"Received Todoist objects: {response}")
        labels = [
            ConcreteTodoistLabel.from_dict(label)  # type: ignore
            for label in response.get("labels", [])
        ]
        filters = [
            ConcreteTodoistFilter.from_dict(filter_)  # type: ignore
            for filter_ in response.get("filters", [])
        ]
        projects = [
            ConcreteTodoistProject.from_dict(project)  # type: ignore
            for project in response.get("projects", [])
        ]

        return ConcreteTodoistObjects(labels=labels, filters=filters, projects=projects)

    def update_todoist_objects(self, todoist_objects: ConcreteTodoistObjects) -> Dict:
        sync_commands = []

        for item in todoist_objects.get_all_items():
            item_type = item.get_type()
            sync_commands.append(self._create_update_command(item_type, item.id, item))

        self.logger.debug(f"Sending update commands: {sync_commands}")
        return self.api_requester.make_request(commands=json.dumps(sync_commands))

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
