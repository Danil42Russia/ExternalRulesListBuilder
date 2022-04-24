from external_rules_list_builder.tools.php_inspections import PhpInspections
from external_rules_list_builder.tools.psalm import Psalm
from external_rules_list_builder.tools.sonarqube import SonarQube
from external_rules_list_builder.tools.tool import Tool


def main() -> None:
    parsers: list[Tool] = [SonarQube(), PhpInspections(), Psalm()]

    for parser in parsers:
        print(parser.get_rules)


if __name__ == "__main__":
    main()
