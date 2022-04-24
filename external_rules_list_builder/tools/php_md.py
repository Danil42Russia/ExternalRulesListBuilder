import requests
from bs4 import BeautifulSoup

from external_rules_list_builder.tools.tool import Tool

GITHUB_RAW_PATH = "https://raw.githubusercontent.com"
REPO_PATH = "phpmd/phpmd"
BRANCH_NAME = "master"
FOLDER_PATH = "src/main/resources/rulesets"

RULES_FILES = [
    "cleancode.xml",
    "codesize.xml",
    "controversial.xml",
    "design.xml",
    "naming.xml",
    "unusedcode.xml",
]


def parse_file(url: str) -> list[str]:
    rules_files: set[str] = set()

    r = requests.get(url)
    r.encoding = "utf-8"

    xml = BeautifulSoup(r.content, features="xml")

    elements = xml.find_all("rule")
    for element in elements:
        rule_name = element.attrs["name"]

        rules_files.add(rule_name)

    return list(rules_files)


def parse_folder() -> list[str]:
    rules_files: set[str] = set()

    BASE_URL = f"{GITHUB_RAW_PATH}/{REPO_PATH}/{BRANCH_NAME}/{FOLDER_PATH}"
    for rules in RULES_FILES:
        file_url = f"{BASE_URL}/{rules}"

        rules_list = parse_file(file_url)
        rules_files |= set(rules_list)

    return list(rules_files)


class PhpMD(Tool):
    @property
    def get_rules(self) -> list[str]:
        return parse_folder()
