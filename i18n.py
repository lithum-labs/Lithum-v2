import os
import re

import yaml
import fire

import config

pattern = r"bot\.translation\.getText\((.*?)\)"


def generate(translations="./translations", lang="ja"):
    ignore_text = 'text="'
    tpath = os.path.join(translations, "{}.yml".format(lang))
    if os.path.isfile(tpath):
        with open(tpath, "r", encoding="utf-8") as f:
            i18n_texts: dict = yaml.safe_load(f)
    else:
        i18n_texts = {"__i18n_meta": {"i18n_version": config.version}}

    with open("./main.py", "r", encoding="utf-8") as f:
        text = f.read()
        match = re.findall(pattern, text)
        if match:
            for i, value in enumerate(match, start=1):
                val = value.strip('"')
                val = val[val.find(ignore_text) + len(ignore_text):]
                i18n_texts.setdefault(val, val)

    source = "./src"
    for file in os.listdir(source):
        if os.path.isfile(os.path.join(source, file)):
            if file.endswith(".py"):
                with open(os.path.join(source, file), "r", encoding="utf-8") as f:
                    text = f.read()
                    match = re.findall(pattern, text)
                    if match:
                        for i, value in enumerate(match, start=1):
                            val = value.strip('"')
                            val = val[val.find(ignore_text) + len(ignore_text):]
                            i18n_texts.setdefault(val, val)

    source = "./lib"
    for file in os.listdir(source):
        if os.path.isfile(os.path.join(source, file)):
            if file.endswith(".py"):
                with open(os.path.join(source, file), "r", encoding="utf-8") as f:
                    text = f.read()
                    match = re.findall(pattern, text)
                    if match:
                        for i, value in enumerate(match, start=1):
                            val = value.strip('"')
                            val = val[val.find(ignore_text) + len(ignore_text):]
                            i18n_texts.setdefault(val, val)

    with open(tpath, "w", encoding="utf-8") as f:
        yaml.safe_dump(i18n_texts, f, allow_unicode=True)


if __name__ == "__main__":
    fire.Fire(generate)
