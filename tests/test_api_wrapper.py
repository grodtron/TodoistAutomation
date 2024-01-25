import unittest
import uuid
from unittest.mock import MagicMock, patch
from autodoist.models import ConcreteTodoistObjects, ConcreteTodoistLabel, ConcreteTodoistFilter, ConcreteTodoistProject
from autodoist.todoist.api_wrapper import TodoistApiWrapper, TodoistAPIRequester

class TestTodoistApiWrapper(unittest.TestCase):

    def setUp(self):
        # Create a MagicMock TodoistAPIRequester for testing
        self.mock_api_requester = MagicMock(spec=TodoistAPIRequester)
        self.todoist_api_wrapper = TodoistApiWrapper(api_requester=self.mock_api_requester)

    def test_get_all_todoist_objects(self):
        # Set up the expected response
        expected_response = {
            "labels": [{"id": 1, "name": "Label 1", "color": "#ffffff", "is_favorite": True}],
            "filters": [{"id": 1, "name": "Filter 1", "query": "query", "color": "#ffffff", "is_favorite": True}],
            "projects": [{"id": 1, "name": "Project 1", "color": "#ffffff", "is_favorite": True}],
        }
        self.mock_api_requester.make_request.return_value = expected_response

        # Call the method to test
        result = self.todoist_api_wrapper.get_all_todoist_objects()

        # Assertions
        self.assertIsInstance(result, ConcreteTodoistObjects)
        self.assertEqual(len(result.labels), 1)
        self.assertEqual(len(result.filters), 1)
        self.assertEqual(len(result.projects), 1)

    def test_update_todoist_objects(self):
        # Set up the expected sync_commands and response
        todoist_objects = ConcreteTodoistObjects(
            labels=[ConcreteTodoistLabel(id=1, name="UpdatedLabel", color="#ffffff", is_favorite=True),
                    ConcreteTodoistLabel(name="NewLabel", color="#ffffff", is_favorite=True)],
            filters=[], #[ConcreteTodoistFilter(id=1, name="Filter 1", query="query", color="#ffffff", is_favorite=True)],
            projects=[] #[ConcreteTodoistProject(id=1, name="Project 1", color="#ffffff", is_favorite=True)]
        )

        # Dummy UUID for mocking
        dummy_uuid = "dummy_uuid"

        expected_commands = [
            {
                "type": "label_update",
                "uuid": dummy_uuid,
                "args": {"id": 1, "color": "#ffffff", "is_favorite": True, "name": "UpdatedLabel"},
            },
            {
                "type": "label_add",
                "uuid": dummy_uuid,
                "temp_id": dummy_uuid,
                "args": {"color": "#ffffff", "is_favorite": True, "name": "UpdatedLabel"},
            },

            # ... similar commands for filters and projects
        ]
        self.mock_api_requester.make_request.return_value = {}

        # Call the method to test
        # Patch the uuid module
        with patch("uuid.uuid4", lambda: dummy_uuid):
            self.todoist_api_wrapper.update_todoist_objects(todoist_objects)
        
        # Assertions
        # Check that make_request was called with a subset of the expected commands
        self.mock_api_requester.make_request.assert_called_once()
        actual_args, actual_kwargs = self.mock_api_requester.make_request.call_args
        actual_commands = actual_kwargs['commands']

        self.assertEqual(len(actual_commands), len(expected_commands))
        
        for actual_command in actual_commands:
            self.assertIn(actual_command, expected_commands)


if __name__ == '__main__':
    unittest.main()
