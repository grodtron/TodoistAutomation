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


class CommandLineInterface:
    def __init__(self, args, yaml_loader, todoist_api_factory, github_poster):
        self.args = args
        self.yaml_loader = yaml_loader
        self.todoist_api_factory = todoist_api_factory
        self.github_poster = github_poster

    def run(self):
        self._setup_logging()
        gtd_state = self._load_gtd_state()
        api_wrapper = self.todoist_api_factory.create_api_wrapper(self.args.api_key)
        existing_state = api_wrapper.get_all_todoist_objects()
        desired_state = process_gtd_state(gtd_state)
        sync_manager = TodoistSyncManager()
        objects_to_update = sync_manager.sync(existing_state, desired_state)

        if self.args.command == "sync":
            api_wrapper.update_todoist_objects(objects_to_update)
        elif self.args.command == "preview":
            self._preview_on_github(objects_to_update)

    def _setup_logging(self):
        level = logging.DEBUG if self.args.debug else logging.INFO
        logging.basicConfig(level=level)

    def _load_gtd_state(self):
        with open(self.args.yaml_file, "r") as f:
            yaml_data = f.read()
        return self.yaml_loader.load_gtd_state(yaml_data)

    def _preview_on_github(self, objects_to_update):
        markdown_summary = render_as_markdown(objects_to_update)
        self.github_poster.post_comment_on_pr(
            self.args.github_token,
            self.args.repo,
            self.args.pr_number,
            markdown_summary,
        )


class TodoistAPIFactory:
    def create_api_wrapper(self, api_key):
        api_requester = TodoistAPIRequester(api_key)
        if args.dry_run:
            return DryRunTodoistApiWrapper(api_requester)
        else:
            return TodoistApiWrapper(api_requester)


class YamlLoader:
    @staticmethod
    def load_gtd_state(yaml_data):
        return load_gtd_state_from_yaml(yaml_data)


class GitHubPoster:
    @staticmethod
    def post_comment_on_pr(github_token, repo, pr_number, comment):
        github = Github(github_token)
        repo = github.get_repo(f"{repo}")
        pr = repo.get_pull(pr_number)
        pr.create_issue_comment(comment)


def main():
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

    args = parser.parse_args()

    cli = CommandLineInterface(
        args,
        YamlLoader(),
        TodoistAPIFactory(),
        GitHubPoster(),
    )
    cli.run()


if __name__ == "__main__":
    main()
