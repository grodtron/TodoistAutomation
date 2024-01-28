import unittest
from unittest.mock import patch, MagicMock
from autodoist.models import GTDState, load_gtd_state_from_yaml

class TestLoadGTDStateFromYAML(unittest.TestCase):

    def test_load_gtd_state_from_yaml(self):
        yaml_data = """
        contexts:
          - name: "Work"
            emojis: "💼"
          - name: "Personal"
            emojis: "🏠"
        composite_contexts:
          - name: "Home"
            labels: ["Family", "Chores"]
          - name: "Office"
            labels: ["Meetings", "Tasks"]
        exclusion_lists:
          - name: "Ignore"
        """
        expected_gtd_state = GTDState(
            contexts=[
                Context(name="Work", emojis="💼"),
                Context(name="Personal", emojis="🏠")
            ],
            composite_contexts=[
                CompositeContext(name="Home", labels=["Family", "Chores"]),
                CompositeContext(name="Office", labels=["Meetings", "Tasks"])
            ],
            exclusion_lists=[
                ExclusionList(name="Ignore")
            ]
        )

        actual_gtd_state = load_gtd_state_from_yaml(yaml_data)
        self.assertEqual(actual_gtd_state, expected_gtd_state)

if __name__ == '__main__':
    unittest.main()
