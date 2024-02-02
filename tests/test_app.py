import unittest
from parameterized import parameterized
from unittest.mock import MagicMock, call
from autodoist.cli import AutoDoistApp
import logging
import json


def make_filter(
    name="Foobar",
    query="somequery",
    color="charcoal",
    is_deleted=False,
    is_favorite=True,
    item_order=1,
):
    return {
        "color": color,
        "id": "2345945708",
        "is_deleted": is_deleted,
        "is_favorite": is_favorite,
        "item_order": item_order,
        "name": name,
        "query": query,
    }


def make_project(
    name="Inbox",
    color="charcoal",
    is_archived=False,
    is_deleted=False,
    is_favorite=False,
):
    return {
        "child_order": 0,
        "collapsed": False,
        "color": color,
        "created_at": "2023-09-24T09:20:22Z",
        "id": "2320352216",
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
    name="Top3", color="charcoal", is_deleted=False, is_favorite=False, item_order=20
):
    return {
        "color": color,
        "id": "2171177815",
        "is_deleted": is_deleted,
        "is_favorite": is_favorite,
        "item_order": item_order,
        "name": name,
    }


def make_hashable_and_comparable(command_dict):
    for uuid_field in ["uuid", "temp_id"]:
        if uuid_field in command_dict:
            command_dict[uuid_field] = "DUMMY_VALUE"

    return json.dumps(command_dict, sort_keys=True)


logging.basicConfig(level=logging.DEBUG)


class TestAutoDoistApp(TestCase):

    @parameterized.expand(
        [
            # Test Case 1
            (
                # YAML input (simplified for brevity)
                """
            contexts:
              - name: "call"
                color: "red"
            composite_contexts:
              - name: "home"
                color: "yellow"
                labels:
                  - "basement"
            exclusion_lists:
              - name: "NotNow"
                color: "grey"
            """,
                # First call response (Get Data Result, simplified)
                {
                    "filters": [make_filter()],
                    "projects": [
                        make_project(),
                        make_project(
                            name="Professional",
                            color="grey",
                            updated_at="2023-12-08T13:01:10Z",
                        ),
                    ],
                    "labels": [make_label(), make_label(name="basement")],
                },
                # Expected Commands Submitted (simplified list of commands)
                [
                    {
                        "type": "label_update",
                        "uuid": "8e5a221f-1cdc-494b-884e-96dbf1710426",
                        "args": {
                            "name": "hardware-store",
                            "color": "green",
                            "is_favorite": True,
                            "id": 2171134071,
                        },
                    },
                    {
                        "type": "project_add",
                        "uuid": "b163d433-b0b5-4349-b06b-f2e41265fbce",
                        "args": {
                            "name": "Waiting",
                            "color": "lavender",
                            "is_favorite": False,
                        },
                        "temp_id": "55acbbdd-f19a-42c5-9bdb-06b59b402767",
                    },
                    # Simplified to only match part of the provided commands for brevity
                ],
            ),
        ]
    )
    def test_auto_doist_app(self, yaml_input, first_call_response, expected_commands):
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
            make_hashable_and_comparable(cmd) for cmd in expected_commands
        }
        actual_commands_set = {
            make_hashable_and_comparable(cmd)
            for cmd in api_requester_mock.make_request.call_args_list[1].kwargs[
                "commands"
            ]
        }

        self.assertEqual(actual_commands_set, expected_commands_set)


if __name__ == "__main__":
    unittest.main()
