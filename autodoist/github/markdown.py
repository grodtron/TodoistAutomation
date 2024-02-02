from autodoist.models import ConcreteTodoistObjects
from typing import List, Dict

def render_as_markdown(todoist_objects: ConcreteTodoistObjects) -> str:
    headers = ["Type", "Operation", "ID", "Name", "Other Attributes"]
    rows = []

    for item in todoist_objects.get_all_items():
        item_type = item.get_type()
        operation = "Update" if item.id else "Create"
        id = item.id if item.id else "N/A"
        name = item.name if hasattr(item, 'name') and item.name else "N/A"
        other_attributes = ", ".join([f"{k}={v}" for k, v in item.__dict__.items() if k not in ['id', 'name'] and v is not None])

        rows.append([item_type, operation, id, name, other_attributes])

    markdown_table = f"| {' | '.join(headers)} |\n"
    markdown_table += f"|{'|'.join(['---' for _ in headers])}|\n"

    for row in rows:
        markdown_table += f"| {' | '.join(str(x) for x in row)} |\n"

    return markdown_table
