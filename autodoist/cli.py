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
        "--debug",
        help="Enable debug level logging project wide.",
        action="store_true",
    )
    
    subparsers = parser.add_subparsers(dest='command', help='sub-command help')

    # Sub-parser for syncing directly to Todoist
    sync_parser = subparsers.add_parser('sync', help='Sync GTD state with Todoist')
    
    # Sub-parser for previewing changes on GitHub
    preview_parser = subparsers.add_parser('preview', help='Preview changes on GitHub')

    preview_parser.add_argument("--github-token", help="GitHub token for authentication.", required=True)

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

    sync_manager = TodoistSyncManager()
    todoist_collection = process_gtd_state(gtd_state)

    # Sync GTD state with Todoist
    objects_to_update = sync_manager.sync(todoist_collection)
    
    if args.command == 'sync':
        api_wrapper.update_todoist_objects(objects_to_update)

    elif args.command == 'preview':

        # Preview changes on GitHub
        markdown_summary = render_as_markdown(todoist_collection)
        # TODO post the markdown summary as a comment on a CR.

if __name__ == "__main__":
    main()
