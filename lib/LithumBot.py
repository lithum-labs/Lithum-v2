from discord.ext import commands

from lib import localization

class LithumBot(commands.Bot):

    def load_translation(self, path: str):
        self.translation = localization.load(path)
