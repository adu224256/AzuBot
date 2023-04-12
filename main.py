import discord
import json
import os

intents = discord.Intents.all()
intents.message_content = True

bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    await load_cogs()
    if bot.auto_sync_commands:
        await bot.sync_commands()
        print("Successfully synced commands!")
    print(f"We have logged in as {bot.user}")


async def load_cogs():
    # 只要是python檔案就會進行載入
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            name = file[:-3]
            print(f'load_extension {name}')
            bot.load_extension(f"cogs.{name}")


with open("api/bot.json", 'r', encoding='utf-8') as f:
    data = json.load(f)
bot.run(data['token'])
