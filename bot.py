from discord.ext import commands, tasks
import discord
import asyncio
from dotenv import load_dotenv
from os import getenv as envv, listdir

from webhook import comp_announcements

load_dotenv()
TOKEN = envv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?')
# bot.remove_command("help")

@bot.event
async def on_ready():
    comp_announcements.start()
    print("Ready!")
"""
@bot.command()
async def s(ctx, event: str = "333", num: str = "1"):
    event = event.lower()
    isevent = False
    for item in events:
        if event in events[item]:
            event = item
            isevent = True
    if int(num) > 5:
        await ctx.send("You cannot generate more than 5 scrambles at a time")
    elif isevent:
        if event[-2:] == "bf":
            event = event[:-2] + "bld"
        response = requests.get(envv("SCRAMBLE_API") + event + envv("SCRAMBLE_NUM") + num)
        data = response.json()
        strsend = "```"
        for i in data["scrambles"]:
            strsend += str(i) + "\n\n"
        strsend += "```"
        await ctx.send(strsend)
    else:
        await ctx.send("Could not match " + event + " to an event.")"""

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await asyncio.sleep(1)
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"{extension} cog reloaded")

for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# bot.loop.create_task(comp_announcements())
bot.run(TOKEN)
