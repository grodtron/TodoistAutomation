from autodoist.models import ConcreteTodoistObjects
from typing import List, Dict


def render_as_markdown(todoist_objects: ConcreteTodoistObjects) -> str:
    markdown = ""

    def _gather_attributes(
        todoist_objects: ConcreteTodoistObjects,
    ) -> Dict[str, List[str]]:
        attributes: Dict[str, List[str]] = {}
        for item in todoist_objects.get_all_items():
            for field_name, field_value in item.to_dict().items():
                if field_value is not None:
                    if field_name not in attributes:
                        attributes[field_name] = []
                    attributes[field_name].append(str(field_value))
        return attributes

    attributes = _gather_attributes(todoist_objects)
    all_fields = sorted(attributes.keys())

    # Ensure 'name' is the leftmost column
    if "name" in all_fields:
        all_fields.remove("name")
        all_fields.insert(0, "name")

    # Ensure 'query' is the rightmost column, if it exists
    if "query" in all_fields:
        all_fields.remove("query")
        all_fields.append("query")

    # Constructing the header row
    markdown += "| " + " | ".join(all_fields) + " |\n"
    markdown += "|-" + "-|-".join(["-" * len(field) for field in all_fields]) + "-|\n"

    # Constructing the rows
    for item in todoist_objects.get_all_items():
        markdown += (
            "| "
            + " | ".join(
                str(item.to_dict().get(field_name, "")) for field_name in all_fields
            )
            + " |\n"
        )

    return markdown
