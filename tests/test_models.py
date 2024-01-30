import unittest
import json
from datetime import datetime
from autodoist.models import ConcreteTodoistProject, TestConcreteTodoistFilter, TestConcreteTodoistLabel

class TestConcreteTodoistLabel(unittest.TestCase):
    def test_from_json(self):
        # Given
        json_data = '''
        {
          "color": "charcoal",
          "id": "2171177815",
          "is_deleted": false,
          "is_favorite": false,
          "item_order": 20,
          "name": "Top3"
        }
        '''

        # When
        label = ConcreteTodoistLabel(**json.loads(json_data))

        # Then
        self.assertEqual(label.color, "charcoal")
        self.assertEqual(label.id, "2171177815")
        self.assertEqual(label.is_deleted, False)
        self.assertEqual(label.is_favorite, False)
        self.assertEqual(label.item_order, 20)
        self.assertEqual(label.name, "Top3")


class TestConcreteTodoistFilter(unittest.TestCase):
    def test_from_json(self):
        # Given
        json_data = '''
        {
          "color": "charcoal",
          "id": "2345486677",
          "is_deleted": false,
          "is_favorite": false,
          "item_order": 21,
          "name": "Today's tasks before 10am",
          "query": "today & due before: 10am & due after: 5am"
        }
        '''

        # When
        filter_obj = ConcreteTodoistFilter(**json.loads(json_data))

        # Then
        self.assertEqual(filter_obj.color, "charcoal")
        self.assertEqual(filter_obj.id, "2345486677")
        self.assertEqual(filter_obj.is_deleted, False)
        self.assertEqual(filter_obj.is_favorite, False)
        self.assertEqual(filter_obj.item_order, 21)
        self.assertEqual(filter_obj.name, "Today's tasks before 10am")
        self.assertEqual(filter_obj.query, "today & due before: 10am & due after: 5am")


class TestConcreteTodoistProject(unittest.TestCase):
    def test_from_json(self):
        # Given
        json_data = """
        {
          "child_order": 0,
          "collapsed": false,
          "color": "charcoal",
          "created_at": "2023-09-24T09:20:22Z",
          "id": "2320352216",
          "inbox_project": true,
          "is_archived": false,
          "is_deleted": false,
          "is_favorite": false,
          "name": "Inbox",
          "parent_id": null,
          "shared": false,
          "sync_id": null,
          "updated_at": "2023-09-24T09:20:22Z",
          "v2_id": "6QXmCv9WvMrJfh33",
          "view_style": "list"
        }
        """

        # When
        project = ConcreteTodoistProject(**json.loads(json_data))

        # Then
        self.assertEqual(project.child_order, 0)
        self.assertEqual(project.collapsed, False)
        self.assertEqual(project.color, "charcoal")
        self.assertEqual(project.id, "2320352216")
        self.assertEqual(project.inbox_project, True)
        self.assertEqual(project.is_archived, False)
        self.assertEqual(project.is_deleted, False)
        self.assertEqual(project.is_favorite, False)
        self.assertEqual(project.name, "Inbox")
        self.assertEqual(project.parent_id, None)
        self.assertEqual(project.shared, False)
        self.assertEqual(project.sync_id, None)
        self.assertEqual(project.updated_at, "2023-09-24T09:20:22Z")
        self.assertEqual(project.v2_id, "6QXmCv9WvMrJfh33")
        self.assertEqual(project.view_style, "list")


if __name__ == "__main__":
    unittest.main()
