from autodoist.models import ConcreteTodoistObjects
from typing import List, Dict
import re


def render_as_markdown(todoist_objects: ConcreteTodoistObjects) -> str:
    headers = ["Type", "Operation", "ID", "Name", "New/Changed Attributes"]
    rows = []

    def process_query(query: str) -> str:
        # Replace multiple spaces with {n spaces} and escape pipe characters
        query = re.sub(r" {2,}", lambda x: f" {{{len(x.group())} spaces}} ", query)
        return query.replace("|", "\|")

    for item in todoist_objects.get_all_items():
        item_type = item.get_type()
        operation = "🌳🔄" if item.id else "🌱✨"
        id = item.id if item.id else " "
        name = item.name
        other_attributes = ", ".join(
            [
                f"{k}=`{process_query(v)}`" if k == "query" else f"{k}={v}"
                for k, v in item.__dict__.items()
                if k not in ["id", "name"] and v is not None
            ]
        )

        rows.append([item_type, operation, id, name, other_attributes])

    markdown_table = f"| {' | '.join(headers)} |\n"
    markdown_table += f"|{'|'.join(['---' for _ in headers])}|\n"

    for row in rows:
        markdown_table += f"| {' | '.join(str(x) for x in row)} |\n"

    return markdown_table
