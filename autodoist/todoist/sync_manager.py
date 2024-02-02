from autodoist.todoist.api_wrapper import TodoistApiWrapper
from autodoist.models import (
    ConcreteTodoistObjects,
    ConcreteTodoistLabel,
    ConcreteTodoistFilter,
    ConcreteTodoistProject,
    TodoistCollection,
)


class TodoistSyncManager:
    def __init__(self):
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

    def _sync_objects(self, existing_objects, desired_objects, concrete_class):
        existing_objects_dict = {obj.name: obj for obj in existing_objects}
        objects_to_sync = []

        for desired_obj in desired_objects:
            existing_obj = existing_objects_dict.get(desired_obj.name)

            if existing_obj is None:
                # Object doesn't exist, create it
                objects_to_sync.append(concrete_class.from_dict(desired_obj.to_dict()))  # type: ignore
            else:
                # Object exists, update it with only the differing attributes
                print("desired")
                print(desired_obj.to_json())
                print("existing")
                print(existing_obj.to_json())
                
                updated_attrs = {
                    attr: value
                    for attr, value in desired_obj.to_dict().items()
                    if getattr(existing_obj, attr) != value
                }
                print("Updates:")
                print(repr(updated_attrs))
                if updated_attrs:
                    updated_attrs["id"] = existing_obj.id
                    updated_attrs["name"] = desired_obj.name
                    updated_obj = concrete_class.from_dict(updated_attrs)
                    objects_to_sync.append(updated_obj)

        return objects_to_sync
