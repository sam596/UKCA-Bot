import discord
import os
from discord.ext import commands
from .lib import helpers as helper

class dev_tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True, description="get message data")
    async def ping(self, ctx):
        await ctx.send(ctx.guild.members[0:2])

    @commands.command(description = "delete last x messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, num: int = 1):
        if num > 10:
            ctx.send("You cannot delete more than 10 messages at a time.")
        else:
            await ctx.channel.purge(limit=num+1)

def setup(client):
    client.add_cog(dev_tools(client))
