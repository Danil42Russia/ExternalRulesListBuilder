import json
import os
from pathlib import Path

from external_rules_list_builder import git, markdown
from external_rules_list_builder.markdown import Row
from external_rules_list_builder.tools.php_inspections import PhpInspections
from external_rules_list_builder.tools.php_md import PhpMD
from external_rules_list_builder.tools.php_stan import PhpStan
from external_rules_list_builder.tools.psalm import Psalm
from external_rules_list_builder.tools.sonarqube import SonarQube
from external_rules_list_builder.tools.tool import Tool


def get_save_path() -> Path:
    workspace_path_str = os.getenv("RUNNER_WORKSPACE")
    if workspace_path_str is None:
        workspace_path = Path(__file__).parent.parent.resolve()
    else:
        workspace_path = Path(workspace_path_str)

    return workspace_path / "build" / "external-rules-list"


def main() -> None:
    rows: list[Row] = []

    save_path = get_save_path()

    git.clone(str(save_path))

    parsers: list[Tool] = [SonarQube(), PhpInspections(), Psalm(), PhpMD(), PhpStan()]
    for parser in parsers:
        rules = sorted(sorted(parser.get_rules), key=len)
        file_name = f"{parser.file_name}.json"

        all_count = len(rules)
        excluded = 0
        implemented = 0

        remaining = all_count - excluded - implemented
        row: Row = {
            "tool_name": f"[{parser.name}]({file_name})",
            "rules_count": all_count,
            "excluded_count": excluded,
            "implemented_count": implemented,
            "remaining_count": remaining,
        }
        rows.append(row)

        out_file = save_path / file_name
        out_file.write_text(json.dumps(rules, indent=2), encoding="utf-8")
        git.add(str(save_path), str(out_file))

    out = markdown.table_generator(rows)
    readme_path = save_path / "README.md"
    readme_path.write_text(out, encoding="utf-8")
    git.add(str(save_path), str(readme_path))

    git.commit(str(save_path))
    git.push(str(save_path))


if __name__ == "__main__":
    main()
