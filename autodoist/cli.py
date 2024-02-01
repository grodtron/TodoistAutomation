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
from autodoist.github.markdown import render_as_markdown
from github import Github


def parse_arguments():
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

    subparsers = parser.add_subparsers(dest="command", help="sub-command help")

    sync_parser = subparsers.add_parser("sync", help="Sync GTD state with Todoist")

    preview_parser = subparsers.add_parser("preview", help="Preview changes on GitHub")
    preview_parser.add_argument(
        "--github-token", help="GitHub token for authentication.", required=True
    )
    preview_parser.add_argument(
        "--repo", help="Name of the GitHub repository.", required=True
    )
    preview_parser.add_argument(
        "--pr-number",
        help="PR number on the GitHub repository.",
        required=True,
        type=int,
    )

    return parser.parse_args()


class GitHubClient:
    def __init__(self, github_token):
        self.github = Github(github_token)

    def post_comment(self, repo, pr_number, comment):
        repo = self.github.get_repo(repo)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment)


class AutoDoistApp:
    def __init__(self, file_reader, todoist_api_wrapper, github_client):
        self.file_reader = file_reader
        self.todoist_api_wrapper = todoist_api_wrapper
        self.github_client = github_client

    def run(self, args):
        yaml_data = self.file_reader(args.yaml_file)
        gtd_state = load_gtd_state_from_yaml(yaml_data)

        desired_state = process_gtd_state(gtd_state)
        existing_state = self.todoist_api_wrapper.get_all_todoist_objects()
        objects_to_update = TodoistSyncManager().sync(existing_state, desired_state)

        if args.command == "sync":
            self.todoist_api_wrapper.update_todoist_objects(objects_to_update)
        elif args.command == "preview":
            markdown_summary = render_as_markdown(objects_to_update)
            self.github_client.post_comment(args.repo, args.pr_number, markdown_summary)


def main():
    args = parse_arguments()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    file_reader = lambda file_path: open(file_path, "r").read()
    api_requester = TodoistAPIRequester(args.api_key)
    todoist_api_wrapper = TodoistApiWrapper(api_requester) if not args.dry_run else DryRunTodoistApiWrapper(api_requester)
    github_client = GitHubClient(args.github_token)

    app = AutoDoistApp(file_reader, todoist_api_wrapper, github_client)
    app.run(args)


if __name__ == "__main__":
    main()
