import unittest
from autodoist.gtd.gtd_state import process_gtd_state, GTDState, TodoistCollection, TodoistLabel, TodoistFilter, TodoistProject, Context, CompositeContext, ExclusionList

class TestGTDState(unittest.TestCase):
    def test_render_todoist_objects(self):

        self.maxDiff = None

        # Create some test data
        context1 = Context(name="Work", emojis="🚀", color="blue")
        context2 = CompositeContext(name="Personal", emojis="🌟", color="green", labels=["Health", "Finance"])

        # Create an instance of GTDState and add the test data
        gtd_state = GTDState(contexts=[context1], composite_contexts=[context2], exclusion_lists=[ExclusionList(name="NotNow")])
        
        # Call the method you want to test
        result = process_gtd_state(gtd_state)

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
        context1 = Context(name="Work", emojis="🚀", color="blue")
        context2 = CompositeContext(name="Personal", emojis="🌟", color="green", labels=["Health", "Finance"])

        # Create an instance of GTDState and add the test data with multiple exclusion lists
        gtd_state = GTDState(contexts=[context1], composite_contexts=[context2], exclusion_lists=[ExclusionList(name="NotNow", color="red"), ExclusionList(name="Vacation", color="blue")])

        # Call the method you want to test
        result = process_gtd_state(gtd_state)

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
            TodoistProject(name="NotNow", color="red", is_favorite=False),
            TodoistProject(name="Vacation", color="blue", is_favorite=False),
        ]

        self.assertEqual(result.labels, expected_labels)
        self.assertEqual(result.filters, expected_filters)
        self.assertEqual(result.projects, expected_projects)

if __name__ == '__main__':
    unittest.main()


