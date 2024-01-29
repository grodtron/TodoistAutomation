import argparse
import yaml
from autodoist.gtd.gtd_state import process_gtd_state
from autodoist.models import load_gtd_state_from_yaml
from autodoist.todoist.api_wrapper import TodoistAPIRequester, TodoistApiWrapper
from autodoist.todoist.sync_manager import TodoistSyncManager


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Command line tool for syncing GTD state with Todoist."
    )
    parser.add_argument(
        "--yaml-file", help="Path to the YAML file containing GTD state.", required=True
    )
    parser.add_argument("--api-key", help="API key for Todoist.", required=True)
    args = parser.parse_args()

    # Load GTD state from YAML file
    with open(args.yaml_file, "r") as f:
        yaml_data = f.read()
    gtd_state = load_gtd_state_from_yaml(yaml_data)

    # Initialize Todoist components
    api_requester = TodoistAPIRequester(args.api_key)
    api_wrapper = TodoistApiWrapper(api_requester)
    sync_manager = TodoistSyncManager(api_wrapper)

    # Process GTD state and sync with Todoist
    todoist_collection = process_gtd_state(gtd_state)
    sync_manager.sync(todoist_collection)


if __name__ == "__main__":
    main()
