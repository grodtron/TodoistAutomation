import unittest
from parameterized import parameterized
from unittest.mock import MagicMock, call
from autodoist.cli import AutoDoistApp
import logging
import json
import re
from typing import Dict, Any, Optional


def make_filter(
    name: str = "Foobar",
    query: str = "somequery",
    color: str = "charcoal",
    is_deleted: bool = False,
    is_favorite: bool = True,
    item_order: int = 1,
    id: int = 123,
) -> Dict[str, Any]:
    return {
        "color": color,
        "id": id,
        "is_deleted": is_deleted,
        "is_favorite": is_favorite,
        "item_order": item_order,
        "name": name,
        "query": query,
    }


def make_project(
    name: str = "Inbox",
    color: str = "charcoal",
    is_archived: bool = False,
    is_deleted: bool = False,
    is_favorite: bool = False,
    id: int = 123,
) -> Dict[str, Any]:
    return {
        "child_order": 0,
        "collapsed": False,
        "color": color,
        "created_at": "2023-09-24T09:20:22Z",
        "id": id,
        "inbox_project": True,
        "is_archived": is_archived,
        "is_deleted": is_deleted,
        "is_favorite": is_favorite,
        "name": name,
        "parent_id": None,
        "shared": False,
        "sync_id": None,
        "updated_at": "2023-09-24T09:20:22Z",
        "v2_id": "6QXmCv9WvMrJfh33",
        "view_style": "list",
    }


def make_label(
    name: str = "Top3",
    color: str = "charcoal",
    is_deleted: bool = False,
    is_favorite: bool = False,
    item_order: int = 20,
    id: int = 123,
) -> Dict[str, Any]:
    return {
        "color": color,
        "id": id,
        "is_deleted": is_deleted,
        "is_favorite": is_favorite,
        "item_order": item_order,
        "name": name,
    }


def make_add_command(type: str, **kwargs: Any) -> Dict[str, Any]:
    return {
        "type": f"{type}_add",
        "args": kwargs,
        "uuid": "fixed-uuid-for-add",
        "temp_id": "fixed-temp-id-for-add",
    }


def make_update_command(type: str, **kwargs: Any) -> Dict[str, Any]:
    return {
        "type": f"{type}_update",
        "args": kwargs,
        "uuid": "fixed-uuid-for-update",
    }


def make_hashable_and_comparable(command_dict: Dict[str, Any]) -> str:
    for uuid_field in ["uuid", "temp_id"]:
        if uuid_field in command_dict:
            command_dict[uuid_field] = "DUMMY_VALUE"

    def _normalize_whitespace(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    if "query" in command_dict["args"]:
        command_dict["args"]["query"] = _normalize_whitespace(
            command_dict["args"]["query"]
        )

    return json.dumps(command_dict, sort_keys=True)


logging.basicConfig(level=logging.DEBUG)


class TestAutoDoistApp(unittest.TestCase):

    @parameterized.expand(  # type: ignore
        [
            # Test Case 1
            (
                # YAML input (simplified for brevity)
                """
            contexts:
              - name: "call"
                color: "red"
            exclusion_lists:
              - name: "NotNow"
                color: "grey"
            """,
                # First call response (Get Data Result, simplified)
                {
                    "filters": [],
                    "projects": [
                        make_project(
                            name="NotNow",
                            color="grey",
                        ),
                    ],
                    "labels": [make_label(name="call", color="yellow", id=123)],
                },
                # Expected Commands Submitted (simplified list of commands)
                [
                    make_update_command("label", name="call", color="red", id=123),
                    make_add_command(
                        "filter",
                        name=" Call",
                        color="red",
                        query="#call | (@call & !#NotNow)",
                        is_favorite=True,
                    ),
                    # Simplified to only match part of the provided commands for brevity
                ],
            ),
        ]
    )
    def test_auto_doist_app(
        self,
        yaml_input: str,
        first_call_response: Dict[str, Any],
        expected_commands: Dict[str, Any],
    ) -> None:
        # Mock the file reader
        file_reader_mock = MagicMock(return_value=yaml_input)

        # Initialize TodoistAPIRequester mock
        api_requester_mock = MagicMock()
        api_requester_mock.make_request.side_effect = [
            first_call_response,
            {},  # TODO
        ]

        # Mock GitHubClient if it's part of your test, otherwise set it up accordingly
        github_client_mock = MagicMock()

        # Set up your application with mocked dependencies
        app = AutoDoistApp(file_reader_mock, api_requester_mock, github_client_mock)

        # Mock command line arguments as needed
        args = MagicMock()
        args.command = "sync"  # Adjust based on the scenario being tested
        args.dry_run = False

        # Execute the application logic
        app.run(args)

        # Verify make_request was called correctly
        self.assertEqual(api_requester_mock.make_request.call_count, 2)
        self.assertEqual(
            api_requester_mock.make_request.call_args_list[0],
            call(sync_token="*", resource_types='["labels", "filters", "projects"]'),
        )

        expected_commands_set = {
            make_hashable_and_comparable(cmd) for cmd in expected_commands  # type: ignore[arg-type]
        }
        actual_commands_set = {
            make_hashable_and_comparable(cmd)
            for cmd in json.loads(
                api_requester_mock.make_request.call_args_list[1].kwargs["commands"]
            )
        }

        self.assertEqual(actual_commands_set, expected_commands_set)


if __name__ == "__main__":
    unittest.main()
