from typing import List, Union, Type, Callable, Any, Dict, Tuple
from dataclasses import dataclass
from autodoist.models import TodoistLabel, TodoistFilter, TodoistProject, TodoistCollection, Context, CompositeContext, ExclusionList, GTDState

def process_gtd_state(gtd_state: GTDState) -> TodoistCollection:
    labels = []
    filters = []
    projects = []

    for context in gtd_state.contexts:
        labels_, filters_, projects_ = _generate_todoist_objects_gtd_context(context, gtd_state.exclusion_lists)
        labels.extend(labels_)
        filters.extend(filters_)
        projects.extend(projects_)

    for composite_context in gtd_state.composite_contexts:
        labels_, filters_, projects_ = _generate_todoist_objects_composite_context(composite_context, gtd_state.exclusion_lists)
        labels.extend(labels_)
        filters.extend(filters_)
        projects.extend(projects_)

    for exclusion_list in gtd_state.exclusion_lists:
        projects_ = _generate_todoist_objects_exclusion_list(exclusion_list)
        projects.extend(projects_)

    return TodoistCollection(labels=labels, filters=filters, projects=projects)

def _generate_todoist_objects_gtd_context(context: Context, exclusion_lists: List[ExclusionList]) -> Tuple[List[TodoistLabel], List[TodoistFilter], List[TodoistProject]]:
    exclusion_queries = ' & '.join([f'!#{exclusion.name}' for exclusion in exclusion_lists])
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
    return [label], [filter_], []

def _generate_todoist_objects_composite_context(context: CompositeContext, exclusion_lists: List[ExclusionList]) -> Tuple[List[TodoistLabel], List[TodoistFilter], List[TodoistProject]]:
    labels = [TodoistLabel(
        name=f"{label}",
        color=context.color,
        is_favorite=True
    ) for label in context.labels]
    exclusion_queries = ' & '.join([f'!#{exclusion.name}' for exclusion in exclusion_lists])
    filter_query = ','.join([f"#{label}{' ' * 60}| (@{label} & {exclusion_queries})" for label in [context.name] + context.labels])
    filter_ = TodoistFilter(
        name=f"{context.emojis} {context.name.title()}",
        query=filter_query,
        color=context.color,
        is_favorite=True
    )
    return labels, [filter_], []

def _generate_todoist_objects_exclusion_list(exclusion_list: ExclusionList) -> List[TodoistProject]:
    project = TodoistProject(
        name=f"{exclusion_list.name}",
        color=exclusion_list.color,
        is_favorite=False
    )
    return [project]
