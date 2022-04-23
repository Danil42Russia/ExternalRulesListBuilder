import requests
from requests_html import HTML

from external_rules_list_builder.tools.tool import Tool

SONAR_URL = "https://rules.sonarsource.com/php"
RULES_PREFIX_CLASS = "RulesListStyled"
PHP_PREFIX = "/php/"


def parsing() -> list[str]:
    rules_list: set[str] = set()

    r = requests.get(SONAR_URL)
    r.encoding = "utf-8"

    html = HTML(html=r.content)

    elements = html.find("li")
    for element in elements:
        class_names: tuple[str] | None = element.attrs.get("class")
        if class_names is None:
            continue

        is_rules_element = any([cn.startswith(RULES_PREFIX_CLASS) for cn in class_names])
        if not is_rules_element:
            continue

        links = element.links
        if len(links) != 1:
            continue

        rules_link = links.pop()
        rules_id = rules_link.replace(PHP_PREFIX, "")

        rules_list.add(rules_id)

    return list(rules_list)


class SonarQube(Tool):
    @property
    def get_rules(self) -> list[str]:
        return parsing()
