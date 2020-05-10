import discord
from discord.ext import commands
from .lib import helpers as helper
from os import getenv as envv
import requests

class scrambles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def s(self, ctx, event: str = "333", num: str = "1"):
        if int(num) > 5:
            await ctx.send("You cannot generate more than 5 scrambles at a time")
            return
        eventcheck = (await helper.event_check(ctx, event))
        if eventcheck[0]:
            return
        event = eventcheck[1]
        if event[-2:] == "bf":
            event = event[:-2] + "bld"
        response = requests.get(envv("SCRAMBLE_API") + event + envv("SCRAMBLE_NUM") + num)
        data = response.json()
        strsend = "```"
        for i in data["scrambles"]:
            strsend += str(i) + "\n\n"
        strsend += "```"
        await ctx.send(strsend)

def setup(client):
    client.add_cog(scrambles(client))
