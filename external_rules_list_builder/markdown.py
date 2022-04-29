from typing import TypedDict


class Row(TypedDict):
    tool_name: str
    rules_count: int
    excluded_count: int
    implemented_count: int
    remaining_count: int


def _final_count(rows: list[Row]) -> Row:
    """Подсчитывает итоговое количество правил"""
    keys = [key for key in rows[0].keys() if key != "tool_name"]
    tmp: Row = {"tool_name": "**Итого**"}

    for key in keys:
        tmp[key] = sum(item[key] for item in rows)

    return tmp


def table_generator(rows: list[Row]) -> str:
    out = ""

    out += "| Название | Количество правил | Исключено правил | Реализовано правил | Оставшиеся правила |\n"
    out += "|:---------|:-----------------:|:----------------:|:------------------:|:------------------:|\n"

    row_style = "|{tool_name}|{rules_count}|{excluded_count}|{implemented_count}|{remaining_count}|\n"

    rows.append(_final_count(rows))
    for row in rows:
        out += row_style.format(**row)

    return out
