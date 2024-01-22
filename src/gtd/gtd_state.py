from typing import Callable, Type, Union
from .models import TodoistLabel, TodoistFilter, TodoistCollection, GTDContext, CompositeContext

class GTDState:
    def __init__(self):
        self.contexts: List[Union[GTDContext, CompositeContext]] = []

    def add_context(self, context: Union[GTDContext, CompositeContext]):
        self.contexts.append(context)

    def _generate_todoist_objects(self, context: Union[GTDContext, CompositeContext]):
        generators = {
            GTDContext: self._generate_todoist_objects_gtd_context,
            CompositeContext: self._generate_todoist_objects_composite_context
        }

        generator = generators[type(context)]
        return generator(context)

    def _generate_todoist_objects_gtd_context(self, context: GTDContext):
        label = TodoistLabel(
            name=f"{context.name}",
            color=context.color,
            is_favorite=True
        )
        filter_ = TodoistFilter(
            name=f"{context.emojis} {context.name.title()}",
            query=f"#{context.name}{' ' * 60}| (@{context.name} & !#NotNow)",
            color=context.color,
            is_favorite=True
        )
        return [label], [filter_]

    def _generate_todoist_objects_composite_context(self, context: CompositeContext):
        labels = [TodoistLabel(
            name=f"{label}",
            color=context.color,
            is_favorite=True
        ) for label in context.labels]
        filter_query = ','.join([f"#{label}{' ' * 60}| (@{label} & !#NotNow)" for label in [context.name] + context.labels])
        filter_ = TodoistFilter(
            name=f"{context.emojis} {context.name.title()}",
            query=filter_query,
            color=context.color,
            is_favorite=True
        )
        return labels, [filter_]

    def render_todoist_objects(self) -> TodoistCollection:
        labels = []
        filters = []

        for context in self.contexts:
            generated_labels, generated_filters = self._generate_todoist_objects(context)
            labels.extend(generated_labels)
            filters.extend(generated_filters)

        return TodoistCollection(labels=labels, filters=filters)

