import re
import sys
import urllib.request as r

number = sys.argv[1]
page = r.urlopen(f'https://github.com/pewpewlive/ppl-i18n/pull/{number}.diff').read().decode('utf8')
filename = page.split(" ")[2][2:]

def parse(filename):
  parsed_strings = {}
  with open(filename, 'r', encoding="utf8") as file:
    lines = file.readlines()
    for line in lines:
      if line.startswith("msgid"):
        id_text = line.rstrip()[7:-1]
        str_text = lines[lines.index(line) + 1].rstrip()[8:-1]

        if str_text == '':
          continue

        id_color_count = len(re.findall(
          r'(?:#(?:[0-9a-fA-F]{2}){4})', id_text))
        str_color_count = len(re.findall(
          r'(?:#(?:[0-9a-fA-F]{2}){4})', str_text))
        id_s_count = id_text.count("%s")
        str_s_count = str_text.count("%s")

        parsed_strings[id_text] = {"condition": "colors_invalid" if id_color_count != str_color_count else 
                                                "s_invalid" if id_s_count != str_s_count else "0",
                                   "line": lines.index(line) + 1,
                                   "id": id_text,
                                   "str": str_text}

    return parsed_strings

strings = parse(filename)
final_output = ""

for key in strings:
  if strings[key]["condition"] == "colors_invalid":
    final_output += f'w // col // {strings[key]["line"]} // {strings[key]["id"]} // {strings[key]["str"]} /// '
  elif strings[key]["condition"] == "s_invalid":
    final_output += f'e // s // {strings[key]["line"]} // {strings[key]["id"]} // {strings[key]["str"]} /// '

final_output += "0"
print(final_output)