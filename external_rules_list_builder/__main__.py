import json
import os
from pathlib import Path

from external_rules_list_builder import git, markdown
from external_rules_list_builder.markdown import Row
from external_rules_list_builder.tools.php_clean import PhpClean
from external_rules_list_builder.tools.php_inspections import PhpInspections
from external_rules_list_builder.tools.php_md import PhpMD
from external_rules_list_builder.tools.php_stan import PhpStan
from external_rules_list_builder.tools.psalm import Psalm
from external_rules_list_builder.tools.sonarqube import SonarQube
from external_rules_list_builder.tools.tool import Tool


def get_workspace_folder() -> Path:
    workspace_path_str = os.getenv("RUNNER_WORKSPACE")
    if workspace_path_str is None:
        workspace_path = Path(__file__).parent.parent.resolve()
    else:
        workspace_path = Path(workspace_path_str)

    return workspace_path


def get_save_path() -> Path:
    workspace_path = get_workspace_folder()

    return workspace_path / "build" / "external-rules-list"


def get_implemented(tool_name: str) -> list[str]:
    implemented_folder = Path("implemented")
    implemented_file_path = get_workspace_folder() / implemented_folder / f"{tool_name}.json"
    if not implemented_file_path.exists():
        return []

    exclude_rules = json.loads(implemented_file_path.read_text(encoding="utf-8"))
    return exclude_rules


def main() -> None:
    rows: list[Row] = []

    save_path = get_save_path()
    git_service = git.Git(save_path)

    git_service.clone()

    parsers: list[Tool] = [SonarQube(), PhpInspections(), Psalm(), PhpMD(), PhpStan(), PhpClean()]
    for parser in parsers:
        rules = sorted(sorted(parser.get_rules), key=len)
        file_name = f"{parser.file_name}.json"
        implemented_rules = get_implemented(parser.file_name)

        all_count = len(rules)
        excluded = 0
        implemented = len(implemented_rules)

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
        git_service.add(str(out_file))

    out = markdown.table_generator(rows)
    readme_path = save_path / "README.md"
    readme_path.write_text(out, encoding="utf-8")
    git_service.add(str(readme_path))

    if git_service.is_can_commit():
        git_service.commit()
        git_service.push()


if __name__ == "__main__":
    main()
