import unittest
from parameterized import parameterized
from autodoist.models import TodoistCollection, TodoistLabel, TodoistFilter, TodoistProject, ConcreteTodoistObjects, ConcreteTodoistLabel, ConcreteTodoistFilter, ConcreteTodoistProject, ConcreteTodoistCollection
from autodoist.todoist.api_wrapper import TodoistApiWrapper
from autodoist.sync_manager import TodoistSyncManager

class TestTodoistSyncManager(unittest.TestCase):

    @parameterized.expand([
        # Test case 1: No changes in desired state
        ("NoChanges", TodoistCollection(
            labels=[TodoistLabel(name="Label1")],
            filters=[TodoistFilter(name="Filter1", query="query1")],
            projects=[TodoistProject(name="Project1")]
        ), ConcreteTodoistCollection(
            labels=[ConcreteTodoistLabel(name="Label1")],
            filters=[ConcreteTodoistFilter(name="Filter1", query="query1")],
            projects=[ConcreteTodoistProject(name="Project1")]
        ), ConcreteTodoistCollection(
            labels=[], filters=[], projects=[]
        )),

        # Test case 2: Adding a new label
        ("AddNewLabel", TodoistCollection(
            labels=[TodoistLabel(name="Label1"), TodoistLabel(name="NewLabel")],
            filters=[TodoistFilter(name="Filter1", query="query1")],
            projects=[TodoistProject(name="Project1")]
        ), ConcreteTodoistCollection(
            labels=[ConcreteTodoistLabel(name="Label1")],
            filters=[ConcreteTodoistFilter(name="Filter1", query="query1")],
            projects=[ConcreteTodoistProject(name="Project1")]
        ), ConcreteTodoistCollection(
            labels=[ConcreteTodoistLabel(name="NewLabel")],
            filters=[], projects=[]
        )),

        # Test case 3: Updating an existing filter
        ("UpdateExistingFilter", TodoistCollection(
            labels=[TodoistLabel(name="Label1")],
            filters=[TodoistFilter(name="Filter1", query="updated_query")],
            projects=[TodoistProject(name="Project1")]
        ), ConcreteTodoistCollection(
            labels=[ConcreteTodoistLabel(name="Label1")],
            filters=[ConcreteTodoistFilter(name="Filter1", query="query1")],
            projects=[ConcreteTodoistProject(name="Project1")]
        ), ConcreteTodoistCollection(
            labels=[], filters=[], projects=[ConcreteTodoistProject(name="Project1")]
        )),
    ])
    def test_sync(self, name, desired_state, existing_state, expected_sync_commands):
        # Arrange
        class MockApiWrapper(TodoistApiWrapper):
            def get_all_todoist_objects(self):
                return existing_state

            def update_todoist_objects(self, concrete_objects):
                self.updated_objects = concrete_objects

        mock_api_wrapper = MockApiWrapper()

        # Act
        sync_manager = TodoistSyncManager(mock_api_wrapper)
        sync_manager.sync(desired_state)

        # Assert
        self.assertEqual(mock_api_wrapper.updated_objects, expected_sync_commands)


if __name__ == '__main__':
    unittest.main()
