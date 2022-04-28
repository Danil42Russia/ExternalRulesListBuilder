import neon
import requests

from external_rules_list_builder.tools.tool import Tool

GITHUB_RAW_PATH = "https://raw.githubusercontent.com"
REPO_PATH = "phpstan/phpstan-src"
BRANCH_NAME = "1.7.x"
FOLDER_PATH = "conf"

RULES_FILES = [f"config.level{i}.neon" for i in range(10)]


def parse_services(conditional_tags: dict, services: list[dict]):
    rules_files: set[str] = set()
    phpstan_tag = "phpstan.rules.rule"

    for service in services:
        class_name = service["class"]

        if phpstan_tag in service.get("tags", ""):
            rules_files.add(class_name)
            continue

        if class_name not in conditional_tags:
            continue

        if phpstan_tag in conditional_tags[class_name]:
            rules_files.add(class_name)
            continue

    return rules_files


def parse_file(url: str) -> list[str]:
    rules_files: set[str] = set()

    r = requests.get(url)
    r.encoding = "utf-8"

    config = neon.parse(r.text)
    for rule in config.get("rules", []):
        rules_files.add(rule)

    conditionalTags = config.get("conditionalTags", [])
    services = config.get("services", [])

    services_rules = parse_services(conditionalTags, services)
    rules_files |= services_rules

    return list(rules_files)


def parse_folder() -> list[str]:
    rules_files: set[str] = set()

    BASE_URL = f"{GITHUB_RAW_PATH}/{REPO_PATH}/{BRANCH_NAME}/{FOLDER_PATH}"
    for rules in RULES_FILES:
        file_url = f"{BASE_URL}/{rules}"

        rules_list = parse_file(file_url)
        rules_files |= set(rules_list)

    return list(rules_files)


class PhpStan(Tool):
    @property
    def get_rules(self) -> list[str]:
        return parse_folder()
