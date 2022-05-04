import subprocess
from datetime import datetime
from pathlib import Path

GIT_REPO = "https://github.com/Danil42Russia/ExternalRulesList.git"


def _commit_message() -> str:
    date = datetime.now().astimezone().replace(microsecond=0).isoformat()
    return f"Committing generated ({date})"


class Git:
    def __init__(self, save_path: Path):
        self.save_path: str = str(save_path)

    def clone(self):
        command = ["git", "clone", GIT_REPO, self.save_path]
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
        command = ["git", "push"]

        proc = subprocess.run(command, cwd=self.save_path)
        if proc.returncode != 0:
            exit(1)
