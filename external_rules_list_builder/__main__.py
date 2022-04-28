from external_rules_list_builder import markdown
from external_rules_list_builder.markdown import Row
from external_rules_list_builder.tools.php_inspections import PhpInspections
from external_rules_list_builder.tools.php_md import PhpMD
from external_rules_list_builder.tools.php_stan import PhpStan
from external_rules_list_builder.tools.psalm import Psalm
from external_rules_list_builder.tools.sonarqube import SonarQube
from external_rules_list_builder.tools.tool import Tool


def main() -> None:
    rows: list[Row] = []

    parsers: list[Tool] = [SonarQube(), PhpInspections(), Psalm(), PhpMD(), PhpStan()]
    for parser in parsers:
        rules = parser.get_rules

        all_count = len(rules)
        excluded = 0
        implemented = 0

        remaining = all_count - excluded - implemented
        row: Row = {
            "tool_name": parser.name,
            "rules_count": all_count,
            "excluded_count": excluded,
            "implemented_count": implemented,
            "remaining_count": remaining,
        }
        rows.append(row)

    markdown.table_generator(rows)


if __name__ == "__main__":
    main()
