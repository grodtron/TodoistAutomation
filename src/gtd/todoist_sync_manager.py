class TodoistSyncManager:
    API_URL = "https://api.todoist.com/sync/v9/sync"
    HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer YOUR_API_KEY_HERE",  # Replace with your Todoist API key
    }

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.sync_commands = []

    def sync(self, todoist_collection: TodoistCollection):
        existing_resources = self._get_existing_resources()

        # Check for existing items and update/create accordingly
        for item_type, collection in [("label", todoist_collection.labels), ("filter", todoist_collection.filters)]:
            for item in collection:
                existing_item = next(
                    (existing for existing in existing_resources[item_type + 's'] if existing["name"] == item.name),
                    None,
                )
                item_id = existing_item.get("id")
                self._create_update_item(item_type, item_id, item)

        # Batched request
        self._make_batched_sync_request()

    def _get_existing_resources(self):
        response = self._make_sync_request(sync_token="*", resource_types=["labels", "filters"])
        return {resource_type: response[resource_type] for resource_type in ["labels", "filters"]}

    def _make_sync_request(self, sync_token, resource_types=None):
        payload = {
            "token": self.api_key,
            "sync_token": sync_token,
            "resource_types": resource_types,
        }
        response = requests.post(self.API_URL, headers=self.HEADERS, data=payload)
        return response.json()

    def _create_update_item(self, item_type, item_id, updated_item):
        action_type = "update" if item_id else "add"
        command = {
            "type": f"{item_type}_{action_type}",
            "uuid": str(uuid.uuid4()),  # Generate a unique UUID for the command
            "args": {"id": item_id} if item_id else {"temp_id": str(uuid.uuid4())},
            **updated_item.to_dict(),
        }
        self.sync_commands.append(command)

    def _make_batched_sync_request(self):
        batched_payload = {"commands": self.sync_commands}
        response = requests.post(self.API_URL, headers=self.HEADERS, json=batched_payload)
        print(response.json())  # Print or handle the response as needed


# Example usage
if __name__ == "__main__":
    todoist_collection = TodoistCollection(
        labels=[TodoistLabel(name="Work"), TodoistLabel(name="Personal")],
        filters=[TodoistFilter(name="Urgent", query="priority:1")],
    )

    sync_manager = TodoistSyncManager(api_key="YOUR_TODOIST_API_KEY")
    sync_manager.sync(todoist_collection)
