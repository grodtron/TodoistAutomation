from typing import List, Union, Type, Callable, Any, Dict, Tuple
from dataclasses import dataclass
from autodoist.models import (
    TodoistLabel,
    TodoistFilter,
    TodoistProject,
    TodoistCollection,
    Context,
    CompositeContext,
    ExclusionList,
    GTDState,
)
from functools import reduce
from itertools import chain


def process_gtd_state(gtd_state: GTDState) -> TodoistCollection:
    def _merge_collections(
        collection1: TodoistCollection, collection2: TodoistCollection
    ) -> TodoistCollection:
        return TodoistCollection(
            labels=collection1.labels + collection2.labels,
            filters=collection1.filters + collection2.filters,
            projects=collection1.projects + collection2.projects,
        )

    def _process_context(context: Context) -> TodoistCollection:
        exclusion_queries = " & ".join(
            [f"!#{exclusion.name}" for exclusion in gtd_state.exclusion_lists]
        )
        label = TodoistLabel(
            name=f"{context.name}", color=context.color, is_favorite=False
        )
        filter_ = TodoistFilter(
            name=f"{context.emojis} {context.name.title()}",
            query=f"#{context.name}{' ' * 60}| (@{context.name} & {exclusion_queries})",
            color=context.color,
            is_favorite=True,
        )
        return TodoistCollection(labels=[label], filters=[filter_], projects=[])

    def _process_composite_context(context: CompositeContext) -> TodoistCollection:
        labels = [
            TodoistLabel(name=f"{label}", color=context.color, is_favorite=False)
            for label in context.labels
        ]
        exclusion_queries = " & ".join(
            [f"!#{exclusion.name}" for exclusion in gtd_state.exclusion_lists]
        )
        filter_query = ",".join(
            [
                f"#{label}{' ' * 60}| (@{label} & {exclusion_queries})"
                for label in [context.name] + context.labels
            ]
        )
        filter_ = TodoistFilter(
            name=f"{context.emojis} {context.name.title()}",
            query=filter_query,
            color=context.color,
            is_favorite=True,
        )
        return TodoistCollection(labels=labels, filters=[filter_], projects=[])

    def _process_exclusion_list(exclusion_list: ExclusionList) -> TodoistCollection:
        project = TodoistProject(
            name=f"{exclusion_list.name}", color=exclusion_list.color, is_favorite=False
        )
        return TodoistCollection(labels=[], filters=[], projects=[project])

    # Use map to generate collections for each context, composite context, and exclusion list
    return reduce(
        _merge_collections,
        chain(
            map(_process_context, gtd_state.contexts),
            map(_process_composite_context, gtd_state.composite_contexts),
            map(_process_exclusion_list, gtd_state.exclusion_lists),
        ),
    )
