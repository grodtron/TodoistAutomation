import unittest
from unittest.mock import MagicMock
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
            labels=[ConcreteTodoistLabel(id=1, name="Label 1", color="#ffffff", is_favorite=True)],
            filters=[ConcreteTodoistFilter(id=1, name="Filter 1", query="query", color="#ffffff", is_favorite=True)],
            projects=[ConcreteTodoistProject(id=1, name="Project 1", color="#ffffff", is_favorite=True)]
        )
        expected_sync_commands = [
            {
                "type": "label_update",
                "uuid": "some_uuid",
                "args": {"id": 1, "color": "#ffffff", "is_favorite": True},
                "id": 1,
                "name": "Label 1"
            },
            # ... similar commands for filters and projects
        ]
        self.mock_api_requester.make_request.return_value = {}

        # Call the method to test
        self.todoist_api_wrapper.update_todoist_objects(todoist_objects)

        # Assertions
        self.mock_api_requester.make_request.assert_called_once_with(commands=expected_sync_commands)

if __name__ == '__main__':
    unittest.main()
