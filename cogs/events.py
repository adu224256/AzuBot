from discord.ext import commands
import json
import discord


class VerifyView(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = user

    @discord.ui.button(label="加入身分組", style=discord.ButtonStyle.success)
    async def move_role_callback(self, button, interaction):
        # Code to move role goes here
        member = interaction.guild.get_member(self.user.id)
        with open('items/roles.json', 'r') as f:
            self.roles_id = json.load(f)['vtuber']

        role = interaction.guild.get_role(
            self.roles_id)  # 將ROLE_ID改成你要加入的身分組的ID
        await member.add_roles(role)
        await interaction.message.delete()

    @discord.ui.button(label="取消審核", style=discord.ButtonStyle.red)
    async def delete_message_callback(self, button, interaction):
        # Code to delete message goes here
        await interaction.message.delete()


class Members_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('items/channel.json', 'r', encoding='utf-8')as f:
            data = json.load(f)
            self.welcome_channel_id = data['welcome']
            self.notice_channel_id = data['notice']

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.bot.get_channel(self.welcome_channel_id)
        notice_channel = self.bot.get_channel(self.notice_channel_id)
        await welcome_channel.send(f'٩(๑•̀ω•́๑)۶ 歡迎光臨 {member.mention} 進入咖啡廳，請先至 {notice_channel.mention} 閱讀入店須知！')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        welcome_channel = self.bot.get_channel(self.welcome_channel_id)
        await welcome_channel.send(f'{member.mention} 離開了咖啡廳，我們懷念他 ヽ(゜▽゜　)－C<(/;◇;)/~[拖走] ')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(reaction)


class Role_add_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open('items/message_id.json', 'r') as f:
            self.mes_id = json.load(f)['role']

        with open('items/roles.json', 'r') as f:
            self.roles = json.load(f)

        with open('items/channel.json', 'r', encoding='utf-8')as f:
            self.verify_channel_id = json.load(f)['verify']

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, user_data):
        if user_data.message_id == self.mes_id:
            if str(user_data.emoji) == "✅":
                # 取得伺服器
                guild = self.bot.get_guild(user_data.guild_id)
                # 指定身分組
                role = guild.get_role(self.roles['member'])
                await user_data.member.add_roles(role)

            if str(user_data.emoji) == "🥚":
                verify_channel = self.bot.get_channel(self.verify_channel_id)
                embed = discord.Embed(
                    title="身分組驗證資訊",
                    description="點選下方按鈕進行身分組驗證",
                    color=discord.Colour.blurple()
                )
                embed.add_field(
                    name='使用者名稱',
                    value=f'{user_data.member.mention}'
                )
                if user_data.member.avatar:
                    embed.set_thumbnail(url=user_data.member.avatar)
                await verify_channel.send(embed=embed, view=VerifyView(user_data.member))


def setup(bot):
    bot.add_cog(Members_events(bot))
    bot.add_cog(Role_add_events(bot))
