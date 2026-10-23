import json

from streamstats.constants import INDENT


def make_report(args: dict[str, object], path: str) -> None:
    """Make a report in json from args"""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(args, file, ensure_ascii=False, indent=INDENT)
        file.write("\n")
