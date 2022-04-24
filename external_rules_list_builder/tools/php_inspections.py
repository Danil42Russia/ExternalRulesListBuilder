import requests
from requests_html import HTML

from external_rules_list_builder.tools.tool import Tool

GITHUB_RAW_PATH = "https://raw.githubusercontent.com"
REPO_PATH = "kalessil/phpinspectionsea"
BRANCH_NAME = "master"
FILE_PATH = "src/main/resources/META-INF/plugin.xml"


def parse() -> list[str]:
    rules_list: set[str] = set()

    URL = f"{GITHUB_RAW_PATH}/{REPO_PATH}/{BRANCH_NAME}/{FILE_PATH}"

    r = requests.get(URL)
    r.encoding = "utf-8"

    html = HTML(html=r.content)

    elements = html.find("localInspection")
    for element in elements:
        rule_name = element.attrs["shortname"]

        rules_list.add(rule_name)

    return list(rules_list)


class PhpInspections(Tool):
    @property
    def get_rules(self) -> list[str]:
        return parse()
