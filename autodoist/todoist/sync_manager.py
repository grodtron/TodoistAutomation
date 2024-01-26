from autodoist.todoist.api_wrapper import TodoistApiWrapper
from autodoist.models import ConcreteTodoistObjects, ConcreteTodoistLabel, ConcreteTodoistFilter, ConcreteTodoistProject, TodoistCollection


class TodoistSyncManager:
    def __init__(self, api_wrapper: TodoistApiWrapper):
        self.api_wrapper = api_wrapper

    def sync(self, desired_state: TodoistCollection):
        """
        Query the api_wrapper for existing objects,
        check for desired objects with matching names
        generate corresponding ConcreteTodoist* objects in a ConcreteTodoistCollection
        use api_wrapper update function to create or update the desired objects
        """
        existing_state = self.api_wrapper.get_all_todoist_objects()

        # Process Labels
        labels_to_sync = self._sync_objects(existing_state.labels, desired_state.labels, ConcreteTodoistLabel)

        # Process Filters
        filters_to_sync = self._sync_objects(existing_state.filters, desired_state.filters, ConcreteTodoistFilter)

        # Process Projects
        projects_to_sync = self._sync_objects(existing_state.projects, desired_state.projects, ConcreteTodoistProject)

        # Execute sync commands
        self.api_wrapper.update_todoist_objects(ConcreteTodoistObjects(
            labels=labels_to_sync,
            filters=filters_to_sync,
            projects=projects_to_sync
        ))

    def _sync_objects(self, existing_objects, desired_objects, concrete_class):
        existing_objects_dict = {obj.name: obj for obj in existing_objects}
        objects_to_sync = []

        for desired_obj in desired_objects:
            existing_obj = existing_objects_dict.get(desired_obj.name)

            if existing_obj is None:
                # Object doesn't exist, create it
                objects_to_sync.append(concrete_class(**desired_obj.to_dict())
            else:
                # Object exists, update it
                updated_obj = concrete_class(**existing_obj.to_dict(), **desired_obj.to_dict())
                objects_to_sync.append(updated_obj)

        return objects_to_sync
