from external_rules_list_builder.tools.php_inspections import PhpInspections
from external_rules_list_builder.tools.php_md import PhpMD
from external_rules_list_builder.tools.php_stan import PhpStan
from external_rules_list_builder.tools.psalm import Psalm
from external_rules_list_builder.tools.sonarqube import SonarQube
from external_rules_list_builder.tools.tool import Tool


def main() -> None:
    parsers: list[Tool] = [SonarQube(), PhpInspections(), Psalm(), PhpMD(), PhpStan()]

    for parser in parsers:
        rules = parser.get_rules

        print(f"{parser.file_name} - {parser.name} - {len(rules)}")


if __name__ == "__main__":
    main()
