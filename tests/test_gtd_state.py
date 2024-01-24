import unittest
from src.gtd.gtd_state import GTDState, TodoistCollection, TodoistLabel, TodoistFilter, TodoistProject, GTDContext, CompositeContext, ExclusionList

class TestGTDState(unittest.TestCase):
    def test_render_todoist_objects(self):

        self.maxDiff = None

        # Create some test data
        context1 = GTDContext(name="Work", emojis="🚀", color="blue")
        context2 = CompositeContext(name="Personal", emojis="🌟", color="green", labels=["Health", "Finance"])

        # Create an instance of GTDState and add the test data
        gtd_state = GTDState()
        gtd_state.add_context(context1)
        gtd_state.add_context(context2)
        gtd_state.add_context(ExclusionList(name="NotNow"))

        # Call the method you want to test
        result = gtd_state.render_todoist_objects()

        # Assert that the result is of the expected type
        self.assertIsInstance(result, TodoistCollection)

        # Assert that the result contains the expected labels and filters
        expected_labels = [
            TodoistLabel(name="Work", color="blue", is_favorite=True),
            TodoistLabel(name="Health", color="green", is_favorite=True),
            TodoistLabel(name="Finance", color="green", is_favorite=True),
        ]

        expected_filters = [
            TodoistFilter(name="🚀 Work", query=f"#Work{' ' * 60}| (@Work & !#NotNow)", color="blue", is_favorite=True),
            TodoistFilter(name="🌟 Personal", query=f"#Personal{' ' * 60}| (@Personal & !#NotNow),#Health{' ' * 60}| (@Health & !#NotNow),#Finance{' ' * 60}| (@Finance & !#NotNow)", color="green", is_favorite=True),
        ]

        self.assertEqual(result.labels, expected_labels)
        self.assertEqual(result.filters, expected_filters)

    def test_render_todoist_objects_multiple_exclusion_lists(self):

        self.maxDiff = None

        # Create some test data
        context1 = GTDContext(name="Work", emojis="🚀", color="blue")
        context2 = CompositeContext(name="Personal", emojis="🌟", color="green", labels=["Health", "Finance"])

        # Create an instance of GTDState and add the test data with multiple exclusion lists
        gtd_state = GTDState()
        gtd_state.add_context(context1)
        gtd_state.add_context(context2)
        gtd_state.add_context(ExclusionList(name="NotNow", color="red"))
        gtd_state.add_context(ExclusionList(name="Vacation", color="blue"))

        # Call the method you want to test
        result = gtd_state.render_todoist_objects()

        # Assert that the result is of the expected type
        self.assertIsInstance(result, TodoistCollection)

        # Assert that the result contains the expected labels and filters with multiple exclusion lists
        expected_labels = [
            TodoistLabel(name="Work", color="blue", is_favorite=True),
            TodoistLabel(name="Health", color="green", is_favorite=True), 
            TodoistLabel(name="Finance", color="green", is_favorite=True),
        ]

        expected_filters = [
            TodoistFilter(name="🚀 Work", query=f"#Work{' ' * 60}| (@Work & !#NotNow & !#Vacation)", color="blue", is_favorite=True),
            TodoistFilter(name="🌟 Personal", query=f"#Personal{' ' * 60}| (@Personal & !#NotNow & !#Vacation),#Health{' ' * 60}| (@Health & !#NotNow & !#Vacation),#Finance{' ' * 60}| (@Finance & !#NotNow & !#Vacation)", color="green", is_favorite=True),
        ]

        expected_projects = [
            TodoistProject(name="NotNow", color="red"),
            TodoistProject(name="Vacation", color="blue"),
        ]

        self.assertEqual(result.labels, expected_labels)
        self.assertEqual(result.filters, expected_filters)
        self.assertEqual(result.projects, expected_projects)

if __name__ == '__main__':
    unittest.main()


