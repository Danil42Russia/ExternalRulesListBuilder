import json
from pathlib import Path

from external_rules_list_builder import git, markdown
from external_rules_list_builder.markdown import Row
from external_rules_list_builder.tools.php_inspections import PhpInspections
from external_rules_list_builder.tools.php_md import PhpMD
from external_rules_list_builder.tools.php_stan import PhpStan
from external_rules_list_builder.tools.psalm import Psalm
from external_rules_list_builder.tools.sonarqube import SonarQube
from external_rules_list_builder.tools.tool import Tool

# fixme: поменять 300iq костыль
SAVE_PATH = Path("C:\\Users\\danda\\source\\open-source\\ExternalRulesListBuilder\\build\\external-rules-list")


def main() -> None:
    rows: list[Row] = []

    git.clone(str(SAVE_PATH))

    parsers: list[Tool] = [SonarQube(), PhpInspections(), Psalm(), PhpMD(), PhpStan()]
    for parser in parsers:
        rules = sorted(sorted(parser.get_rules), key=len)

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

        out_file = SAVE_PATH / f"{parser.file_name}.json"
        out_file.write_text(json.dumps(rules, indent=2), encoding="utf-8")
        git.add(str(SAVE_PATH), str(out_file))

    out = markdown.table_generator(rows)
    readme_path = SAVE_PATH / "README.md"
    readme_path.write_text(out, encoding="utf-8")
    git.add(str(SAVE_PATH), str(readme_path))

    git.commit(str(SAVE_PATH))
    git.push(str(SAVE_PATH))


if __name__ == "__main__":
    main()
