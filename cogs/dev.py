import discord
import os
from discord.ext import commands
from .lib import helpers as helper
import re

class dev_tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, description="get message data")
    async def ping(self, ctx):
        for user in ctx.guild.members:
            try:
                if re.match("^[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}$", user.nick[-10:]):
                    try:
                        await ctx.send(user.nick[-10:])
                    except:
                        await ctx.send("Failed for user " + user.nick)
                else:
                    await ctx.send("Failed for user " + user.nick)
            except:
                await ctx.send("Failed for user " + user.name)              

    @commands.command(description = "delete last x messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num: int = 1):
        if num > 10:
            ctx.send("You cannot delete more than 10 messages at a time.")
        else:
            await ctx.channel.purge(limit=num+1)

def setup(client):
    client.add_cog(dev_tools(client))
