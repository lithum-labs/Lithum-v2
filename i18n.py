import os
import re

import yaml
import fire

pattern = r"self\.bot\.translation\.getText\((.*?)\)"

def generate(source="./src", translations="./translations", lang="ja"):
    tpath = os.path.join(translations, "{}.yml".format(lang))
    if os.path.isfile(tpath):
        with open(tpath, "r", encoding="utf-8") as f:
            i18n_texts = yaml.safe_load(f)
    else:
        i18n_texts = {}

    for file in os.listdir(source):
        if os.path.isfile(os.path.join(source, file)):
            if file.endswith(".py"):
                with open(os.path.join(source, file), "r", encoding="utf-8") as f:
                    text = f.read()
                    match = re.findall(pattern, text)
                    if match:
                        for i, value in enumerate(match, start=1):
                            val = value.strip('"')
                            i18n_texts[val] = val

    with open(tpath, "w", encoding="utf-8") as f:
        yaml.safe_dump(i18n_texts, f, allow_unicode=True)

if __name__ == "__main__":
    fire.Fire(generate)