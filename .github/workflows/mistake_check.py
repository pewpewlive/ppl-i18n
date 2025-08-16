import re
import sys
import urllib.request as r
import json


def main():
    page: list[str] = (
        r.urlopen(f"https://github.com/pewpewlive/ppl-i18n/pull/{sys.argv[1]}.diff")
        .read()
        .decode("utf8")
        .split("\n")
    )

    filename = page[0].split(" ")[2][2:]
    page = page[4:]

    strings = parse(page)
    final_output = json.dumps(strings, ensure_ascii=False)

    print(final_output)


def color_check(id_text: str, str_text: str) -> bool:
    color_regex = re.compile(r"#(?:[0-9a-fA-F]{2}){4}")
    id_color_count = len(re.findall(color_regex, id_text))
    str_color_count = len(re.findall(color_regex, str_text))

    return id_color_count == str_color_count


def format_check(id_text: str, str_text: str) -> bool:
    format_specifier_regex = re.compile(r"%s|%([1-9][0-9]*)\$s")
    id_s = re.findall(format_specifier_regex, id_text)
    str_s = re.findall(format_specifier_regex, str_text)
    id_s.sort()
    str_s.sort()

    return id_s == str_s


def condition(valid_colors: bool, valid_format: bool) -> str:
    if not valid_colors and not valid_format:
        return "invalid_colors_and_format"
    elif not valid_colors:
        return "invalid_colors"
    elif not valid_format:
        return "invalid_format"
    elif not valid_format:
        return "invalid_format"
    else:
        return ""


def parse(page: list[str]):
    id_text: str = ""
    current_line_number: int = 0
    parsed_strings: list[dict[str, int | str]] = []
    for line in page:
        if line.startswith("@@"):
            current_line_number = int(line.split(" ")[1][1:].split(",")[0]) - 1
            continue

        current_line_number += 1
        if line.startswith(" msgid") or line.startswith("-msgid"):
            id_text = line.rstrip()[8:-1]
            continue

        if line.startswith("-msgstr"):
            current_line_number -= 1
            continue

        if line.startswith("+msgid") and id_text != "":
            parsed_strings.append(
                {
                    "condition": "modified_msgid",
                    "line": current_line_number - 1,
                    "id": id_text,
                    "str": line.rstrip()[8:-1],
                }
            )
            continue

        if not line.startswith("+msgstr"):
            continue

        str_text = line.rstrip()[9:-1]
        if str_text == "":
            continue

        valid_colors = color_check(id_text, str_text)
        valid_format = format_check(id_text, str_text)
        if not valid_colors or not valid_format:
            parsed_strings.append(
                {
                    "condition": condition(valid_colors, valid_format),
                    "line": current_line_number,
                    "id": id_text,
                    "str": str_text,
                }
            )

    return parsed_strings


if __name__ == "__main__":
    main()
