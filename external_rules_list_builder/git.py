import os
import subprocess
from datetime import datetime
from pathlib import Path


def _commit_message() -> str:
    date = datetime.now().astimezone().replace(microsecond=0).isoformat()
    return f"Committing generated ({date})"


class Git:
    def __init__(self, save_path: Path):
        self.save_path: str = str(save_path)

        push_token = os.getenv("PUSH_GITHUB_TOKEN")
        if push_token is None:
            token = ""
        else:
            token = f"{push_token}:x-oauth-basic@"

        self.git_repo: str = f"https://{token}github.com/Danil42Russia/ExternalRulesList.git"

    def clone(self):
        command = ["git", "clone", self.git_repo, self.save_path]
        proc = subprocess.run(command)
        if proc.returncode != 0:
            exit(1)

    def add(self, file_path: str):
        command = ["git", "add", file_path]

        proc = subprocess.run(command, cwd=self.save_path)
        if proc.returncode != 0:
            exit(1)

    def commit(self):
        message = _commit_message()
        command = ["git", "commit", "-m", message]

        proc = subprocess.run(command, cwd=self.save_path)
        if proc.returncode != 0:
            exit(1)

    def is_can_commit(self):
        command = ["git", "status"]
        noting_commit = "nothing to commit, working tree clean"

        proc = subprocess.run(command, cwd=self.save_path, stdout=subprocess.PIPE)
        if proc.returncode != 0:
            exit(1)

        status_out = proc.stdout.decode()
        return noting_commit not in status_out

    def push(self):
        command = ["git", "push", self.git_repo]

        proc = subprocess.run(command, cwd=self.save_path)
        if proc.returncode != 0:
            exit(1)
