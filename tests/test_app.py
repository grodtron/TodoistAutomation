import unittest
from parameterized import parameterized
from unittest.mock import MagicMock, call
from autodoist.cli import (
    AutoDoistApp,
)  # Adjust the import path to your actual module structure

from unittest import TestCase
from parameterized import parameterized
from unittest.mock import MagicMock, call
import logging


import json


def make_hashable_and_comparable(command_dict):
    for uuid_field in ['uuid', 'temp_id']:
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
                    "filters": [
                        "filters":[
                            {
                                "color":"charcoal","id":"2345945708","is_deleted":false,"is_favorite":true,"item_order":1,"name":"Foobar","query":"somequery"
                            },{
                                "color":"charcoal","id":"2345943667","is_deleted":false,"is_favorite":false,"item_order":2,"name":"Test of wizard workflow","query":"#TEST & subtask & today"
                            }
                    ],
                    "projects": "projects":[
                        {
                            "child_order":0,"collapsed":false,"color":"charcoal","created_at":"2023-09-24T09:20:22Z","id":"2320352216","inbox_project":true,"is_archived":false,"is_deleted":false,"is_favorite":false,"name":"Inbox","parent_id":null,"shared":false,"sync_id":null,"updated_at":"2023-09-24T09:20:22Z","v2_id":"6QXmCv9WvMrJfh33","view_style":"list"
                        },{
                            "child_order":0,"collapsed":false,"color":"grey","created_at":"2023-09-24T09:20:34Z","id":"2320352279","is_archived":false,"is_deleted":false,"is_favorite":false,"name":"\ud83d\udcbb Professional","parent_id":null,"shared":false,"sync_id":null,"updated_at":"2023-12-08T13:01:10Z","v2_id":"6QXmCwGR8cffFp7j","view_style":"list"
                        }],
                    "labels":[{
                            "color":"charcoal","id":"2171177815","is_deleted":false,"is_favorite":false,"item_order":20,"name":"Top3"
                        },{
                            "color":"charcoal","id":"2170323972","is_deleted":false,"is_favorite":false,"item_order":19,"name":"basement"
                        },
                },
                # Expected Commands Submitted (simplified list of commands)
                [
                    {'type': 'label_update', 'uuid': '8e5a221f-1cdc-494b-884e-96dbf1710426', 'args': {'name': 'hardware-store', 'color': 'green', 'is_favorite': True, 'id': 2171134071}},
                    {'type': 'project_add', 'uuid': 'b163d433-b0b5-4349-b06b-f2e41265fbce', 'args': {'name': 'Waiting', 'color': 'lavender', 'is_favorite': False}, 'temp_id': '55acbbdd-f19a-42c5-9bdb-06b59b402767'},
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
