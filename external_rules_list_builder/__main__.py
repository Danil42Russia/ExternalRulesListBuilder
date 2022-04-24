from external_rules_list_builder.tools.php_inspections import PhpInspections
from external_rules_list_builder.tools.sonarqube import SonarQube
from external_rules_list_builder.tools.tool import Tool


def main() -> None:
    parsers: list[Tool] = [SonarQube(), PhpInspections()]

    for parser in parsers:
        print(parser.name)


if __name__ == "__main__":
    main()
