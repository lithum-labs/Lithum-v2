from discord.ext import commands

from lib import localization

class LithumBot(commands.AutoShardedBot):

    def load_translation(self, path: str):
        self.translation = localization.load(path)
