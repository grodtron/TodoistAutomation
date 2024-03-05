from typing import Type, List, Dict, Any
from autodoist.todoist.api_wrapper import TodoistApiWrapper
from autodoist.models import (
    ConcreteTodoistObjects,
    ConcreteTodoistLabel,
    ConcreteTodoistFilter,
    ConcreteTodoistProject,
    TodoistCollection,
)


class TodoistSyncManager:
    def __init__(self) -> None:
        pass

    def sync(
        self, existing_state: ConcreteTodoistObjects, desired_state: TodoistCollection
    ) -> ConcreteTodoistObjects:
        """
        Compares existing and desired states to determine objects to sync.
        Returns collections of objects to sync.
        """
        # Process Labels
        labels_to_sync = self._sync_objects(
            existing_state.labels, desired_state.labels, ConcreteTodoistLabel
        )

        # Process Filters
        filters_to_sync = self._sync_objects(
            existing_state.filters, desired_state.filters, ConcreteTodoistFilter
        )

        # Process Projects
        projects_to_sync = self._sync_objects(
            existing_state.projects, desired_state.projects, ConcreteTodoistProject
        )

        return ConcreteTodoistObjects(
            labels=labels_to_sync,
            filters=filters_to_sync,
            projects=projects_to_sync,
        )

    def _sync_objects(
        self,
        existing_objects: List[Any],
        desired_objects: List[Any],
        concrete_class: (
            Type[ConcreteTodoistLabel]
            | Type[ConcreteTodoistFilter]
            | Type[ConcreteTodoistProject]
        ),
    ) -> List[Any]:
        existing_objects_dict: Dict[str, Any] = {
            obj.name: obj for obj in existing_objects
        }
        objects_to_sync: List[Any] = []

        for desired_obj in desired_objects:
            existing_obj = existing_objects_dict.get(desired_obj.name)

            if existing_obj is None:
                # Object doesn't exist, create it
                objects_to_sync.append(concrete_class.from_dict(desired_obj.to_dict()))  # type: ignore
            else:
                # Object exists, update it with only the differing attributes

                desired_dict = desired_obj.to_dict()
                existing_dict = existing_obj.to_dict()

                updated_attrs: Dict[str, Any] = {
                    attr: value
                    for attr, value in desired_dict.items()
                    if existing_dict.get(attr) != value
                }

                if updated_attrs:
                    updated_attrs["id"] = existing_obj.id
                    updated_attrs["name"] = desired_obj.name
                    updated_obj = concrete_class.from_dict(updated_attrs)
                    objects_to_sync.append(updated_obj)

        return objects_to_sync
