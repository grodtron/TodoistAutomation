from autodoist.models import ConcreteTodoistObjects

def render_as_markdown(todoist_objects: ConcreteTodoistObjects) -> str:
    markdown = ""

    for item in todoist_objects.get_all_items():
        action = "Created" if item.id is None else "Updated"
        markdown += f"### {item.get_type().capitalize()} ({action})\n"
        markdown += "| Field | Value |\n"
        markdown += "|-------|-------|\n"
        for field_name, field_value in item.to_dict().items():
            if field_value is not None:
                markdown += f"| {field_name.capitalize().replace('_', ' ')} | {field_value} |\n"
        markdown += "\n"

    return markdown
