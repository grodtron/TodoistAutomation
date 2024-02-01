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
                        {"id": "2345719224", "name": "📞🗣️📲 Call", "color": "red"},
                        # Adding only one filter for simplicity
                    ],
                    "projects": [
                        {"id": "2326905183", "name": "NotNow", "color": "grey"},
                        # Adding only one project for simplicity
                    ],
                },
                # Expected Commands Submitted (simplified list of commands)
                [
                    {
                        "type": "filter_update",
                        "args": {
                            "name": "📞🗣️📲 Call",
                            "color": "red",
                            "id": "2345719224",
                        },
                    },
                    {
                        "type": "project_update",
                        "args": {"name": "NotNow", "color": "grey", "id": "2326905183"},
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

        # Execute the application logic
        app.run(args)

        # Verify make_request was called correctly
        expected_calls = [
            call(sync_token="*", resource_types='["labels", "filters", "projects"]'),
            call(commands=expected_commands),
        ]  # TODO first call args
        api_requester_mock.make_request.assert_has_calls(
            expected_calls, any_order=False
        )

        # Assert the number of calls if necessary
        self.assertEqual(api_requester_mock.make_request.call_count, 2)


if __name__ == "__main__":
    unittest.main()
