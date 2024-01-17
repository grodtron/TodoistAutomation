# Python Function: Filter Creation

## You
Here is documentation on the Todoist v9 sync API.


Example add filter request:
$ curl https://api.todoist.com/sync/v9/sync \
    -H "Authorization: Bearer 0123456789abcdef0123456789abcdef01234567" \
    -d commands='[
    {
        "type": "filter_add", 
        "temp_id": "9204ca9f-e91c-436b-b408-ea02b3972686", 
        "uuid": "0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8", 
        "args": {
            "name": "Important", 
            "query": "priority 1"
        }
    }]'
Example response:
{
  ...
  "sync_status": {"0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8": "ok"},
  "temp_id_mapping": {"9204ca9f-e91c-436b-b408-ea02b3972686": "4638878"},
  ...
}


Can you please write a Python function to create the json to send to add a filter?

## ChatGPT
Certainly! Here's a simple Python function to create the JSON for adding a filter request:

```python
import json

def create_filter_add_request(name, query):
    request_json = {
        "commands": [
            {
                "type": "filter_add",
                "temp_id": "9204ca9f-e91c-436b-b408-ea02b3972686",
                "uuid": "0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8",
                "args": {
                    "name": name,
                    "query": query
                }
            }
        ]
    }
    return json.dumps(request_json, indent=2)

# Example usage:
name = "Important"
query = "priority 1"
request_json = create_filter_add_request(name, query)
print(request_json)

```

Replace the `name` and `query` variables with your desired filter name and query. The function will return a formatted JSON string that you can use to make the API request.

## You
Please rewrite it so the filter-add struct is not wrapped in commands

## ChatGPT
Certainly! Here's the modified Python function:

```python
import json

def create_filter_add_request(name, query):
    request_json = {
        "type": "filter_add",
        "temp_id": "9204ca9f-e91c-436b-b408-ea02b3972686",
        "uuid": "0b8690b8-59e6-4d5b-9c08-6b4f1e8e0eb8",
        "args": {
            "name": name,
            "query": query
        }
    }
    return json.dumps(request_json, indent=2)

# Example usage:
name = "Important"
query = "priority 1"
request_json = create_filter_add_request(name, query)
print(request_json)

```

In this version, the `filter_add` structure is no longer wrapped in the `commands` list. This function will directly produce the JSON for adding a filter.

## You
And please don’t hardcode the uuids but generate them

## ChatGPT
Certainly! Here's the updated Python function that generates random UUIDs:

```python
import json
import uuid

def create_filter_add_request(name, query):
    temp_id = str(uuid.uuid4())
    filter_uuid = str(uuid.uuid4())

    request_json = {
        "type": "filter_add",
        "temp_id": temp_id,
        "uuid": filter_uuid,
        "args": {
            "name": name,
            "query": query
        }
    }
    return json.dumps(request_json, indent=2)

# Example usage:
name = "Important"
query = "priority 1"
request_json = create_filter_add_request(name, query)
print(request_json)

```

Now, each time you call the function, it will generate new random UUIDs for the `temp_id` and `uuid` fields in the JSON structure.

## You
Please add a Boolean is_favorite property that’s always true, and a user specified color str

## ChatGPT
Certainly! Here's the modified Python function with the added `is_favorite` boolean property and the user-specified `color` string:

```python
import json
import uuid

def create_filter_add_request(name, query, color):
    temp_id = str(uuid.uuid4())
    filter_uuid = str(uuid.uuid4())

    request_json = {
        "type": "filter_add",
        "temp_id": temp_id,
        "uuid": filter_uuid,
        "args": {
            "name": name,
            "query": query,
            "is_favorite": True,
            "color": color
        }
    }
    return json.dumps(request_json, indent=2)

# Example usage:
name = "Important"
query = "priority 1"
color = "red"
request_json = create_filter_add_request(name, query, color)
print(request_json)

```

Now, the function takes an additional parameter `color`, which is a user-specified string for the filter color. The `is_favorite` property is set to `True` by default.

