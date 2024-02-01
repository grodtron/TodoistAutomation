import unittest
from parameterized import parameterized
from unittest.mock import MagicMock, call
from yourmodule import (
    AutoDoistApp,
)  # Adjust the import path to your actual module structure


class TestAutoDoistApp(unittest.TestCase):

    @parameterized.expand(
        [
            (
                "path/to/yaml_file_1",
                {"type": "get", "data": {...}},
                {"type": "update", "data": {...}},
                {"response": "first_call_response_data"},
                {"response": "second_call_response_data"},
            ),
            # Add more sets of parameters for additional test cases
        ]
    )
    def test_auto_doist_app(
        self,
        yaml_input,
        first_call_payload,
        second_call_payload,
        first_call_response,
        second_call_response,
    ):
        # Mock the file reader
        file_reader_mock = MagicMock(return_value=yaml_input)

        # Initialize TodoistAPIRequester mock
        api_requester_mock = MagicMock()
        api_requester_mock.make_request.side_effect = [
            first_call_response,
            second_call_response,
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
        expected_calls = [call(**first_call_payload), call(**second_call_payload)]
        api_requester_mock.make_request.assert_has_calls(
            expected_calls, any_order=False
        )

        # Assert the number of calls if necessary
        self.assertEqual(api_requester_mock.make_request.call_count, 2)


if __name__ == "__main__":
    unittest.main()
