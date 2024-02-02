import unittest
from unittest.mock import MagicMock
from autodoist.github.markdown import render_as_markdown
from autodoist.models import (
    ConcreteTodoistObjects,
    ConcreteTodoistLabel,
    ConcreteTodoistFilter,
    ConcreteTodoistProject,
    Color,
)

import re


def normalize_markdown_table_cell_content(cell):
    cell = cell.strip()

    if cell and cell == "-" * len(cell):
        cell = "------"

    return cell


def normalize_markdown_table(markdown):
    # Convert to lowercase
    markdown = markdown.lower()

    # Normalize columns
    markdown = "\n".join(
        "|".join(map(normalize_markdown_table_cell_content, line.split("|")))
        for line in markdown.splitlines()
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
        self.todoist_objects = ConcreteTodoistObjects(
            labels=[
                ConcreteTodoistLabel(
                    name="Urgent", color=Color.RED, is_favorite=True, id=1
                )
            ],
            filters=[
                ConcreteTodoistFilter(
                    name="Work",
                    query="@work     | (@work & !#NotNow)",
                    color=Color.BLUE,
                    is_favorite=False,
                )
            ],
            projects=[
                ConcreteTodoistProject(
                    name="Personal", color=Color.GREEN, is_favorite=True
                )
            ],
        )

    def test_render_as_markdown(self):
        expected_markdown = """
| Type   | Operation | ID  | Name     | New/Changed Attributes           |
| ------ | --------- | --- | -------- | -------------------------- |
| Label  | 🌳🔄    | 1   | Urgent   | Color=red, Is_favorite=True|
| Filter | 🌱✨    |  | Work     | Query=`@work{5 spaces}| (@work & !#NotNow)`, Color=blue, Is_favorite=False |
| Project| 🌱✨    |  | Personal | Color=green, Is_favorite=True |
"""
        rendered_markdown = render_as_markdown(self.todoist_objects)
        normalized_rendered = normalize_markdown_table(rendered_markdown)
        normalized_expected = normalize_markdown_table(expected_markdown)
        self.assertEqual(normalized_rendered, normalized_expected)


if __name__ == "__main__":
    unittest.main()
