from typing import List, Union
from dataclasses import dataclass
from models import TodoistLabel, TodoistFilter, TodoistProject, TodoistCollection, GTDContext, CompositeContext, ExclusionList

@dataclass
class TodoistObjects:
    labels: List[TodoistLabel]
    filters: List[TodoistFilter]
    projects: List[TodoistProject]

class GTDState:
    def __init__(self):
        self.contexts: List[Union[GTDContext, CompositeContext, ExclusionList]] = []

    def add_context(self, context: Union[GTDContext, CompositeContext, ExclusionList]):
        self.contexts.append(context)

    def _generate_todoist_objects(self, context: Union[GTDContext, CompositeContext, ExclusionList]) -> TodoistObjects:
        generators = {
            GTDContext: self._generate_todoist_objects_gtd_context,
            CompositeContext: self._generate_todoist_objects_composite_context,
            ExclusionList: self._generate_todoist_objects_exclusion_list
        }

        generator = generators[type(context)]
        return generator(context)

    def _generate_todoist_objects_gtd_context(self, context: GTDContext) -> TodoistObjects:
        exclusion_queries = ' & '.join([f'!#{exclusion.name}' for exclusion in self._get_exclusion_lists()])
        label = TodoistLabel(
            name=f"{context.name}",
            color=context.color,
            is_favorite=True
        )
        filter_ = TodoistFilter(
            name=f"{context.emojis} {context.name.title()}",
            query=f"#{context.name}{' ' * 60}| (@{context.name} & {exclusion_queries})",
            color=context.color,
            is_favorite=True
        )
        return TodoistObjects(labels=[label], filters=[filter_], projects=[])

    def _generate_todoist_objects_composite_context(self, context: CompositeContext) -> TodoistObjects:
        labels = [TodoistLabel(
            name=f"{label}",
            color=context.color,
            is_favorite=True
        ) for label in context.labels]
        exclusion_queries = ' & '.join([f'!#{exclusion.name}' for exclusion in self._get_exclusion_lists()])
        filter_query = ','.join([f"#{label}{' ' * 60}| (@{label} & {exclusion_queries})" for label in [context.name] + context.labels])
        filter_ = TodoistFilter(
            name=f"{context.emojis} {context.name.title()}",
            query=filter_query,
            color=context.color,
            is_favorite=True
        )
        return TodoistObjects(labels=labels, filters=[filter_], projects=[])

    def _generate_todoist_objects_exclusion_list(self, exclusion_list: ExclusionList) -> TodoistObjects:
        project = TodoistProject(
            name=f"{exclusion_list.name}",
            color=exclusion_list.color,
            is_favorite=False
        )
        return TodoistObjects(labels=[], filters=[], projects=[project])

    def _get_exclusion_lists(self) -> List[ExclusionList]:
        return [context for context in self.contexts if isinstance(context, ExclusionList)]

    def render_todoist_objects(self) -> TodoistCollection:
        labels = []
        filters = []
        projects = []

        for context in self.contexts:
            generated_objects = self._generate_todoist_objects(context)
            labels.extend(generated_objects.labels)
            filters.extend(generated_objects.filters)
            projects.extend(generated_objects.projects)

        return TodoistCollection(labels=labels, filters=filters, projects=projects)
