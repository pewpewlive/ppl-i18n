import re
import sys
import urllib.request as r
import json

number = sys.argv[1]
page = r.urlopen(
    f'https://github.com/pewpewlive/ppl-i18n/pull/{number}.diff').read().decode("utf8").split('\n')
filename = page[0].split(' ')[2][2:]
page = page[4:]

def parse(page):
    id_text = ""
    current_line_number = 0
    parsed_strings = []
    for line in page:
        if line.startswith("@@"):
            current_line_number = int(line.split(' ')[1][1:].split(',')[0]) - 1
            continue

        current_line_number += 1
        if line.startswith(" msgid"):
            id_text = line.rstrip()[8:-1]
        elif line.startswith("-msgstr"):
            current_line_number -= 1
        elif line.startswith("+msgstr"):
            str_text = line.rstrip()[9:-1]

            if str_text == '':
                continue

            id_color_count = len(re.findall(
                r'(?:#(?:[0-9a-fA-F]{2}){4})', id_text))
            str_color_count = len(re.findall(
                r'(?:#(?:[0-9a-fA-F]{2}){4})', str_text))
            id_s_count = id_text.count("%s")
            str_s_count = str_text.count("%s")

            if id_color_count != str_color_count or id_s_count != str_s_count:
                parsed_strings.append({"condition": "invalid_colors" if id_color_count != str_color_count else
                                                    "invalid_s" if id_s_count != str_s_count else "other",
                                       "line": current_line_number,
                                       "id": id_text,
                                       "str": str_text})

    return parsed_strings


strings = parse(page)
final_output = json.dumps(strings, ensure_ascii=False)

print(final_output)
