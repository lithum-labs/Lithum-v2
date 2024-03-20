from __future__ import annotations

import os

import discord
from discord import app_commands
import yaml

class Localizer(app_commands.Translator):

    async def load(self) -> None:
        transfiles = [
            f
            for f in os.listdir("./translations")
            if os.path.isfile(os.path.join("./translations", f)) and f.endswith(".yml")
        ]
        locales = {}
        available_langs = []
        for trans in transfiles:
            with open(os.path.join("./translations", trans), "r", encoding="utf-8") as f:
                lc = yaml.safe_load(f)
                locales[trans.replace(".yml", "")] = lc
                available_langs.append({"name": lc["__metadata"]["name"], "langId": lc["__metadata"]["langId"]})
        self.locales = locales

    async def unload(self) -> None:
        self.locales = {}

    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext,
    ) -> str | None:
        # For this example, we can translate a few words in Japanese...
        message = str(string)
        if self.locales.get(locale) is None:
            return message
        elif self.locales.get(locale).get(locale) is None:
            return message
        return self.locales[locale][message]

class Translation:
    def __init__(self, locales: dict) -> None:
        self.locales = locales

    def getText(self, text: str, lang: str="ja"):
        text = text.replace("\n", "z{n}")
        if self.locales.get(lang) is None:
            return text.replace("z{n}", "\n")
        elif self.locales.get(lang).get(text) is None:
            return text.replace("z{n}", "\n")
        return self.locales[lang][text].replace("z{n}", "\n")

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