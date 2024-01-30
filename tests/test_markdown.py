import unittest
from autodoist.github.markdown import render_as_markdown
from autodoist.models import ConcreteTodoistObjects, ConcreteTodoistLabel, ConcreteTodoistFilter, ConcreteTodoistProject

class TestRenderAsMarkdown(unittest.TestCase):
    def test_render_as_markdown(self):
        # Create some sample ConcreteTodoistObjects
        label = ConcreteTodoistLabel(name="Label 1", color="red", is_favorite=True)
        filter = ConcreteTodoistFilter(name="Filter 1", query="some query", color="green", is_favorite=False)
        project = ConcreteTodoistProject(name="Project 1", color="blue", is_favorite=True, parent_id=123)

        todoist_objects = ConcreteTodoistObjects(labels=[label], filters=[filter], projects=[project])

        expected_output = """### Label (Created)
| Name | Value |
|-------|-------|
| name | Label 1 |
| color | red |
| is_favorite | True |

### Filter (Created)
| Name | Value |
|-------|-------|
| name | Filter 1 |
| query | some query |
| color | green |
| is_favorite | False |

### Project (Created)
| Name | Value |
|-------|-------|
| name | Project 1 |
| color | blue |
| is_favorite | True |
| parent_id | 123 |
"""

        # Normalize whitespace and capitalization for comparison
        expected_output = '\n'.join([line.strip() for line in expected_output.strip().split('\n')]).lower()
        actual_output = render_as_markdown(todoist_objects)
        actual_output = '\n'.join([line.strip() for line in actual_output.strip().split('\n')]).lower()

        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
