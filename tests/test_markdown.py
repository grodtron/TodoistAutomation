import unittest
from unittest.mock import MagicMock
from autodoist.models import ConcreteTodoistObjects
from autodoist.github.markdown import render_as_markdown

class TestRenderAsMarkdown(unittest.TestCase):
    def setUp(self):
        self.todoist_objects = ConcreteTodoistObjects()
        # Mocking some objects for testing
        mock_item_1 = MagicMock()
        mock_item_1.to_dict.return_value = {'name': 'Task 1', 'priority': 1}
        mock_item_2 = MagicMock()
        mock_item_2.to_dict.return_value = {'name': 'Task 2', 'due_date': '2024-02-01'}
        self.todoist_objects.get_all_items.return_value = [mock_item_1, mock_item_2]

    def test_render_as_markdown(self):
        expected_markdown = "| name | due_date | priority | query |\n"
        expected_markdown += "|------|----------|----------|-------|\n"
        expected_markdown += "| Task 1 |  | 1 |  |\n"
        expected_markdown += "| Task 2 | 2024-02-01 |  |  |\n"

        self.assertEqual(render_as_markdown(self.todoist_objects), expected_markdown)


if __name__ == '__main__':
    unittest.main()
