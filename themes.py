# Copyright 2021 iiPython
# Generates a colors.yml file from the Alacritty Colorscheme Wiki

# Modules
import sys
import string
import requests
from bs4 import BeautifulSoup

# Configuration
url = "https://github.com/alacritty/alacritty/wiki/Color-schemes"
indent = 2

# Initialization
constructed = """# Alacritty Color Schemes
# Taken from (github.com/alacritty/alacritty/wiki/Color-schemes#multiple-schemes)
# Constructed using alacritty-schemes (github.com/ii-Python/alacritty-schemes)
#
# To use this, simply include the file in your alacritty.yml:
#
# include:
# - /path/to/colors.yml
#
# Then set your preferred scheme at the end of the file.

# Color Schemes (yikes!)
schemes:\n"""

data = BeautifulSoup(requests.get(url).text, "html.parser")

# Load themes
themes = []
for elem in data.find_all("details"):
    summary = elem.findChildren("summary", recursive = False)
    if not summary:
        continue

    data = elem.findChildren("div", recursive = False)
    if not data:
        continue

    summary = summary[0]
    link = summary.findChildren("a", recursive = False)
    if not link:
        continue

    # Construct theme name (and remove special chars)
    name = link[0].text.replace(" ", "_").lower().rstrip("_theme")
    for char in string.punctuation.replace("_", ""):
        name = name.replace(char, "")

    # Save theme data
    themes.append({
        "name": name + "_theme",
        "id": name,
        "data": data[0].get("data-snippet-clipboard-copy-content").split("\n")
    })

# Scheme handlers
def remove_comments(scheme: list) -> list:
    lines = []
    for line in scheme:
        if " #" not in line:
            lines.append(line)

        else:
            line = line.split(" #")[0].rstrip()
            lines.append(line)

    return lines

def build_scheme(scheme: list) -> str:
    return "\n".join([line for line in scheme if line.strip()])

def indent(scheme: list, text: str) -> list:
    return [text + line for line in scheme]

def generate_themes(themes: list) -> str:
    return "# Available themes:\n# " + ", ".join([theme["id"] for theme in themes])

# Handle minified schemes
args = sys.argv[1:]
if args and args[0] == "minified":

    # Await input
    print("Place minified scheme in colors.yml and press enter.")
    input()

    # Load data
    with open("colors.yml", "r") as colors:
        data = colors.read().lstrip("{").rstrip("}")

    # Replace theme names
    for theme in themes:
        data = data.replace("*: {".replace("*", theme["name"]), "*: &= {".replace("*", theme["name"]).replace("=", theme["id"]))

    # Rewrite file
    with open("colors.yml", "w") as colors:
        colors.write(constructed[:-1].rstrip("schemes:") + data.rstrip("\n")[:-1] + f"\n{generate_themes(themes)}\ncolors: *material")

    print("Rewrote colors.yml")
    exit(0)

# Rewrite theme file
for theme in themes:
    constructed += build_scheme(indent([f"{theme['name']}: &{theme['id']}"] + [line for line in remove_comments(theme["data"]) if line != "colors:" and not line.startswith("#")], "  ")) + "\n"

# Save
with open("colors.yml", "w+") as file:
    file.write(constructed + f"\n{generate_themes(themes)}\ncolors: *material")

print("Created colors.yml successfully, you can now use it in alacritty.")
