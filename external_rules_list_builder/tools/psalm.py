import requests
from bs4 import BeautifulSoup

from external_rules_list_builder.tools.tool import Tool

GITHUB_RAW_PATH = "https://raw.githubusercontent.com"
REPO_PATH = "vimeo/psalm"
BRANCH_NAME = "4.x"
FILE_PATH = "config.xsd"


def parse() -> list[str]:
    rules_list: set[str] = set()

    URL = f"{GITHUB_RAW_PATH}/{REPO_PATH}/{BRANCH_NAME}/{FILE_PATH}"

    r = requests.get(URL)
    r.encoding = "utf-8"

    xml = BeautifulSoup(r.content, features="xml")

    el = xml.find("xs:complexType", attrs={"name": "IssueHandlersType"})
    elements = el.find_all("xs:element")
    for element in elements:
        rule_name = element.attrs["name"]

        rules_list.add(rule_name)

    return list(rules_list)


class Psalm(Tool):
    @property
    def get_rules(self) -> list[str]:
        return parse()
