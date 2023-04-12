from discord.ext import commands
from core.any import Cog_Extension


class extension(Cog_Extension):

    @commands.is_owner()
    @commands.slash_command(description="upload")
    async def upload(self, ctx, extension):
        try:
            self.bot.load_extension(f'cogs.{extension}')
            await ctx.respond(f'{extension} 已上傳', ephemeral=True)
        except Exception as ex:
            await ctx.respond(ex, ephemeral=True)

    @commands.is_owner()
    @commands.slash_command(description="unload")
    async def unload(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            await ctx.respond(f'{extension} 已卸載', ephemeral=True)
        except Exception as ex:
            await ctx.respond(ex, ephemeral=True)

    @commands.is_owner()
    @commands.slash_command(description="reload")
    async def reload(self, ctx, extension):
        # 如果直接更改程式碼的話就直接reload
        try:
            self.bot.reload_extension(f'cogs.{extension}')
            await ctx.respond(f'{extension} 已更新', ephemeral=True)
        except Exception as ex:
            await ctx.respond(ex, ephemeral=True)


def setup(bot):
    bot.add_cog(extension(bot))
