from typing import Optional, List, Dict, Any, cast
import logging
import uuid
import requests
import json
from autodoist.models import (
    ConcreteTodoistObjects,
    ConcreteTodoistLabel,
    ConcreteTodoistFilter,
    ConcreteTodoistProject,
)


class TodoistAPIRequester:
    API_URL: str = "https://api.todoist.com/sync/v9/sync"

    def __init__(self, api_key: str) -> None:
        self.api_key: str = api_key
        self.logger: logging.Logger = logging.getLogger(__name__)

    def make_request(self, **payload: Any) -> Dict[str, Any]:
        self.logger.debug(f"Sending request to {self.API_URL} with payload: {payload}")
        headers: Dict[str, str] = {"Authorization": f"Bearer {self.api_key}"}
        response: requests.Response = requests.post(
            self.API_URL, headers=headers, data=payload
        )
        self.logger.debug(f"Received response: {response.content.decode('utf-8')}")

        print(response.status_code)
        print(repr(response))

        if response.status_code != 200:
            self.logger.error(
                f"Request failed with status code: {response.status_code}"
            )
            try:
                error_data: Dict[str, Any] = response.json()
                error_message: str = error_data.get("error", "Unknown error")
                error_code: Optional[int] = error_data.get("error_code")
                raise Exception(f"Request failed: {error_message} ({error_code})")
            except ValueError:
                raise Exception("Request failed with unknown error")

        result: Dict[str, Any] = response.json()
        return result


class TodoistApiWrapper:
    def __init__(self, api_requester: TodoistAPIRequester) -> None:
        self.api_requester: TodoistAPIRequester = api_requester
        self.logger: logging.Logger = logging.getLogger(__name__)

    def get_all_todoist_objects(self) -> ConcreteTodoistObjects:
        response: Dict[str, Any] = self.api_requester.make_request(
            sync_token="*", resource_types='["labels", "filters", "projects"]'
        )
        self.logger.debug(f"Received Todoist objects: {response}")
        labels: List[ConcreteTodoistLabel] = [
            cast(ConcreteTodoistLabel, ConcreteTodoistLabel.from_dict(label))  # type: ignore[attr-defined]
            for label in response.get("labels", [])
        ]
        filters: List[ConcreteTodoistFilter] = [
            cast(ConcreteTodoistFilter, ConcreteTodoistFilter.from_dict(filter_))  # type: ignore[attr-defined]
            for filter_ in response.get("filters", [])
        ]
        projects: List[ConcreteTodoistProject] = [
            cast(ConcreteTodoistProject, ConcreteTodoistProject.from_dict(project))  # type: ignore[attr-defined]
            for project in response.get("projects", [])
        ]

        return ConcreteTodoistObjects(labels=labels, filters=filters, projects=projects)

    def update_todoist_objects(
        self, todoist_objects: ConcreteTodoistObjects
    ) -> Dict[str, Any]:
        sync_commands: List[Dict[str, Any]] = []

        for item in todoist_objects.get_all_items():
            item_type: str = item.get_type()
            sync_commands.append(self._create_update_command(item_type, item.id, item))

        self.logger.debug(f"Sending update commands: {sync_commands}")
        return self.api_requester.make_request(commands=json.dumps(sync_commands))

    def _create_update_command(
        self, item_type: str, item_id: Optional[int], updated_item: Any
    ) -> Dict[str, Any]:
        action_type: str = "update" if item_id else "add"
        command: Dict[str, Any] = {
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
    def update_todoist_objects(
        self, todoist_objects: ConcreteTodoistObjects
    ) -> Dict[str, Any]:
        sync_commands: List[Dict[str, Any]] = []

        for item in todoist_objects.get_all_items():
            item_type: str = item.get_type()
            command: Dict[str, Any] = self._create_update_command(
                item_type, item.id, item
            )
            sync_commands.append(command)
            self.logger.debug(f"Dry run command: {command}")

        self.logger.info("Dry run completed. No changes were made.")
        return {}
