import os

import yaml


class Translation:
    def __init__(self, locales: dict) -> None:
        self.locales = locales

    def getText(self, text: str, lang: str="ja"):
        if self.locales.get(lang) is None:
            return text
        elif self.locales.get(lang).get(text) is None:
            return text
        return text

def load(path) -> Translation:
    transfiles = [
        f
        for f in os.listdir(path)
        if os.path.isfile(os.path.join(path, f)) and f.endswith(".yml")
    ]
    locales = {}
    for trans in transfiles:
        with open(os.path.join(path, trans), "r", encoding="utf-8") as f:
            lc = yaml.safe_load(f)
            locales[trans.replace(".yml", "")] = lc
    return Translation(locales)