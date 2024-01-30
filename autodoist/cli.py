import argparse
import logging
import yaml
from autodoist.gtd.gtd_state import process_gtd_state
from autodoist.models import load_gtd_state_from_yaml
from autodoist.todoist.api_wrapper import (
    TodoistAPIRequester,
    TodoistApiWrapper,
    DryRunTodoistApiWrapper,
)
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
    parser.add_argument(
        "--dry-run",
        help="Perform a dry run without making any changes to Todoist.",
        action="store_true",
    )
    parser.add_argument(
        "--dump-only",
        help="Dump the generated todoist_collection without syncing.",
        action="store_true",
    )
    parser.add_argument(
        "--debug",
        help="Enable debug level logging project wide.",
        action="store_true",
    )
    args = parser.parse_args()

    # Set logging level to DEBUG if debug flag is provided
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    # Load GTD state from YAML file
    with open(args.yaml_file, "r") as f:
        yaml_data = f.read()
    gtd_state = load_gtd_state_from_yaml(yaml_data)

    # Initialize Todoist components
    api_requester = TodoistAPIRequester(args.api_key)

    if args.dry_run:
        api_wrapper = DryRunTodoistApiWrapper(api_requester)
    else:
        api_wrapper = TodoistApiWrapper(api_requester)

    sync_manager = TodoistSyncManager(api_wrapper)

    # Process GTD state and sync with Todoist or dump the collection
    todoist_collection = process_gtd_state(gtd_state)

    if args.dump_only:
        print(todoist_collection)
    else:
        sync_manager.sync(todoist_collection)


if __name__ == "__main__":
    main()
