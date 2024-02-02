import unittest
from parameterized import parameterized
from autodoist.models import (
    TodoistCollection,
    TodoistLabel,
    TodoistFilter,
    TodoistProject,
    ConcreteTodoistObjects,
    ConcreteTodoistLabel,
    ConcreteTodoistFilter,
    ConcreteTodoistProject,
)
from autodoist.todoist.api_wrapper import TodoistApiWrapper
from autodoist.todoist.sync_manager import TodoistSyncManager


class TestTodoistSyncManager(unittest.TestCase):

    @parameterized.expand(
        [
            # Test case 1: No changes in desired state
            (
                "NoChanges",
                TodoistCollection(
                    labels=[TodoistLabel(name="Label1")],
                    filters=[TodoistFilter(name="Filter1", query="query1")],
                    projects=[TodoistProject(name="Project1")],
                ),
                ConcreteTodoistObjects(
                    labels=[ConcreteTodoistLabel(id=1, name="Label1")],
                    filters=[
                        ConcreteTodoistFilter(id=2, name="Filter1", query="query1")
                    ],
                    projects=[ConcreteTodoistProject(id=3, name="Project1")],
                ),
                ConcreteTodoistObjects(),
            ),
            # Test case 2: Adding a new label
            (
                "AddNewLabel",
                TodoistCollection(
                    labels=[TodoistLabel(name="Label1"), TodoistLabel(name="NewLabel")],
                    filters=[TodoistFilter(name="Filter1", query="query1")],
                    projects=[TodoistProject(name="Project1")],
                ),
                ConcreteTodoistObjects(
                    labels=[ConcreteTodoistLabel(id=4, name="Label1")],
                    filters=[
                        ConcreteTodoistFilter(id=5, name="Filter1", query="query1")
                    ],
                    projects=[ConcreteTodoistProject(id=6, name="Project1")],
                ),
                ConcreteTodoistObjects(
                    labels=[
                        ConcreteTodoistLabel(name="NewLabel"),
                    ],
                ),
            ),
            # Test case 3: Updating an existing filter
            (
                "UpdateExistingFilter",
                TodoistCollection(
                    labels=[TodoistLabel(name="Label1")],
                    filters=[TodoistFilter(name="Filter1", query="updated_query")],
                    projects=[TodoistProject(name="Project1")],
                ),
                ConcreteTodoistObjects(
                    labels=[ConcreteTodoistLabel(id=7, name="Label1")],
                    filters=[
                        ConcreteTodoistFilter(id=8, name="Filter1", query="query1")
                    ],
                    projects=[ConcreteTodoistProject(id=9, name="Project1")],
                ),
                ConcreteTodoistObjects(
                    filters=[
                        ConcreteTodoistFilter(
                            id=8, name="Filter1", query="updated_query"
                        )
                    ],
                ),
            ),
            # Test case 5: Add a New Filter
            (
                "AddNewFilter",
                TodoistCollection(
                    labels=[],
                    filters=[TodoistFilter(name="NewFilter", query="query2")],
                    projects=[],
                ),
                ConcreteTodoistObjects(),
                ConcreteTodoistObjects(
                    filters=[ConcreteTodoistFilter(name="NewFilter", query="query2")],
                ),
            ),
            # Test case 6: Existing project - no changes
            (
                "NoopProject",
                TodoistCollection(
                    projects=[TodoistProject(name="NotNow", color=Color.GREY)],
                ),
                ConcreteTodoistObjects(
                    projects=[ConcreteTodoistProject(name="NotNow", color=Color.GREY)],
                ),
                ConcreteTodoistObjects(
                    
                ),
            ),
        ]
    )
    def test_sync(self, name, desired_state, existing_state, expected_sync_commands):
        # Act
        sync_manager = TodoistSyncManager()
        actual_sync_commands = sync_manager.sync(existing_state, desired_state)

        # Assert
        self.assertEqual(actual_sync_commands, expected_sync_commands)


if __name__ == "__main__":
    unittest.main()
