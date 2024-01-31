import unittest
from unittest.mock import MagicMock
from autodoist.github.markdown import render_as_markdown

import re


def normalize_markdown_table_cell_content(cell):
    cell = cell.strip()

    if cell == "-" * len(cell):
        cell = "------"

    return cell


def normalize_markdown_table(markdown):
    # Convert to lowercase
    markdown = markdown.lower()

    # Remove extra whitespace (except new lines)
    markdown = re.sub(r"\s+", " ", markdown)

    # Normalize column widths
    markdown = re.sub(
        r"(\|.*?\|)",
        lambda x: "|"
        + "|".join(
            map(normalize_markdown_table_cell_content(cell), x.group(1).split("|"))
        )
        + "|",
        markdown,
    )

    return markdown.strip()


class TestNormalizeMarkdownTable(unittest.TestCase):
    def test_identical_tables(self):
        markdown_table1 = """
        | Name   | Age | Location   |
        |--------|-----|------------|
        | Alice  | 30  | Wonderland |
        | Bob    | 25  | City       |
        """
        markdown_table2 = """
        | Name | Age | Location |
        |------|-----|----------|
        |Alice |30   |Wonderland|
        |Bob   |25   |City      |
        """
        self.assertEqual(
            normalize_markdown_table(markdown_table1),
            normalize_markdown_table(markdown_table2),
        )


class TestRenderAsMarkdown(unittest.TestCase):
    def setUp(self):
        self.todoist_objects = MagicMock()
        # Mocking some objects for testing
        mock_item_1 = MagicMock()
        mock_item_1.to_dict.return_value = {"name": "Task 1", "priority": 1}
        mock_item_2 = MagicMock()
        mock_item_2.to_dict.return_value = {"name": "Task 2", "due_date": "2024-02-01"}
        self.todoist_objects.get_all_items.return_value = [mock_item_1, mock_item_2]

    def test_render_as_markdown(self):
        expected_markdown = "| name | due_date | priority |\n"
        expected_markdown += "|------|----------|----------|\n"
        expected_markdown += "| Task 1 |  | 1 |\n"
        expected_markdown += "| Task 2 | 2024-02-01 |  |\n"

        self.assertEqual(
            normalize_markdown_table(render_as_markdown(self.todoist_objects)),
            normalize_markdown_table(expected_markdown),
        )


if __name__ == "__main__":
    unittest.main()
