import argparse
import logging
from typing import Any, Callable, Dict

import yaml
from github import Github
from autodoist.gtd.gtd_state import process_gtd_state
from autodoist.models import load_gtd_state_from_yaml, GTDState
from autodoist.todoist.api_wrapper import (
    TodoistAPIRequester,
    TodoistApiWrapper,
    DryRunTodoistApiWrapper,
)
from autodoist.todoist.sync_manager import TodoistSyncManager
from autodoist.github.markdown import render_as_markdown


class GitHubClient:
    def __init__(self, github_token: str) -> None:
        self.github = Github(github_token)

    def post_comment(self, repo_name: str, pr_number: int, comment: str) -> None:
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment)


class AutoDoistApp:
    def __init__(
        self,
        file_reader: Callable[[str], str],
        api_requester: TodoistAPIRequester,
        github_client: GitHubClient,
    ) -> None:
        self.file_reader: Callable[[str], str] = file_reader
        self.api_requester: TodoistAPIRequester = api_requester
        self.github_client: GitHubClient = github_client

    def run(self, args: argparse.Namespace) -> None:
        yaml_data: str = self.file_reader(args.yaml_file)
        gtd_state: GTDState = load_gtd_state_from_yaml(yaml_data)

        todoist_api_wrapper: TodoistApiWrapper = (
            TodoistApiWrapper(self.api_requester)
            if not args.dry_run
            else DryRunTodoistApiWrapper(self.api_requester)
        )

        desired_state = process_gtd_state(gtd_state)
        existing_state = todoist_api_wrapper.get_all_todoist_objects()
        objects_to_update = TodoistSyncManager().sync(existing_state, desired_state)

        if args.command == "sync":
            todoist_api_wrapper.update_todoist_objects(objects_to_update)
        elif args.command == "preview":
            markdown_summary = render_as_markdown(objects_to_update)
            self.github_client.post_comment(args.repo, args.pr_number, markdown_summary)


def parse_arguments() -> argparse.Namespace:
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
        "--debug", help="Enable debug level logging project wide.", action="store_true"
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


def main() -> None:
    args = parse_arguments()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    file_reader: Callable[[str], str] = lambda file_path: open(file_path, "r").read()
    api_requester: TodoistAPIRequester = TodoistAPIRequester(args.api_key)
    github_client: GitHubClient = (
        GitHubClient(args.github_token) if hasattr(args, "github_token") else None
    )

    app: AutoDoistApp = AutoDoistApp(file_reader, api_requester, github_client)
    app.run(args)


if __name__ == "__main__":
    main()
