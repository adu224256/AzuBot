from discord.ext import commands

# 這邊可以使用Cog功能繼承基本屬性


class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
