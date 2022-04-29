import subprocess
from datetime import datetime

GIT_REPO = "https://github.com/Danil42Russia/ExternalRulesList.git"


def _commit_message() -> str:
    date = datetime.now().astimezone().replace(microsecond=0).isoformat()
    return f"Committing generated ({date})"


def clone(save_path: str):
    command = ["git", "clone", GIT_REPO, save_path]
    proc = subprocess.run(command)
    if proc.returncode != 0:
        exit(1)


def add(save_path: str, file_path: str):
    command = ["git", "add", file_path]

    proc = subprocess.run(command, cwd=save_path)
    if proc.returncode != 0:
        exit(1)


def commit(save_path: str):
    message = _commit_message()
    command = ["git", "commit", "-m", message]

    proc = subprocess.run(command, cwd=save_path)
    if proc.returncode != 0:
        exit(1)


def push(save_path: str):
    command = ["git", "push"]

    proc = subprocess.run(command, cwd=save_path)
    if proc.returncode != 0:
        exit(1)
