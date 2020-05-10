import discord
import os
from discord.ext import commands
from .lib import helpers as helper

class nickwcaid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def nickwcaid(self, ctx, nick, wcaid, user: discord.Member = ''):
        # checks to see if the user was passed and if the author has permissions
        if (await helper.check_nick_perms(ctx)) and user != '':
            return
        # sets a flag to determine if we are updating the author or another user
        # sets user equal to the author if one was not passed.
        user, isuser = helper.is_user_check(ctx, user)
        # checks to see if the wcaid and nick are the same as the current nickname
        if nick + ' | ' + wcaid == user.nick:
            if isuser:
                await ctx.send("Your nickname and WCA ID are already set.")
            else:
                await ctx.send("Nickname and WCA ID already set.")
            return
        # nicknames must not have a vertical bar
        if (await helper.nick_bar_check(ctx, nick, isuser)):
            return
        # WCA IDs must be capitalised, this does it for the user if they lazy
        wcaid = wcaid.upper()
        if (await helper.no_id_check(ctx, wcaid, isuser)):
            await user.edit(nick=(nick + " | No ID"))
            return
        # checks if the syntax of the WCA ID is valid, if not, it also checks for "No ID"/"NoID", makes the change and returns.
        if (await helper.wcaid_validity_nick(ctx, wcaid, user, isuser)):
            return
        # else, we start the lookup.
        data = (await helper.person_lookup(ctx, wcaid))
        if data is None:
            return
        # finally, edit the user :)
        await user.edit(nick=(f"{nick} | {wcaid}"))
        firstname = data["person"]["name"].split(" ")[0]
        if isuser:
            await ctx.send(f"Your nickname and WCA ID have been updated successfully!\nThanks {firstname}!")
        else:
            await ctx.send(f"{firstname}'s name and WCA ID updated successfully!'")

    @commands.command(pass_context=True)
    async def wcaid(self, ctx, wcaid, user: discord.Member = ''):
        # checks to see if the user was passed and if the author has permissions
        if (await helper.check_nick_perms(ctx)) and user != '':
            return
        # sets a flag to determine if we are updating the author or another user
        # sets user equal to the author if one was not passed.
        user, isuser = helper.is_user_check(ctx, user)
        # user's WCA ID might already be set.
        if user.display_name.find(" | " + wcaid) != -1:
            if isuser:
                await ctx.send("Your WCA ID is already set.")
            else:
                await ctx.send("WCA ID already set.")
            return
        # if the user somehow has a vertical bar in their name already,
        # we force them to change both nick and wca id at the same time
        # so that it can be removed before adding a WCA ID
        if user.display_name.find("|") != -1:
            await ctx.send("Please use ?nickwcaid")
            return
        # WCA IDs must be capitalised, this does it for the user if they lazy
        wcaid = wcaid.upper()
        if (await helper.no_id_check(ctx, wcaid, isuser)):
            await user.edit(nick=(user.display_name[:-5] + wcaid))
        # checks if the syntax of the WCA ID is valid,
        # if not, it also checks for "No ID"/"NoID", makes the change and returns.
        if (await helper.wcaid_validity_nick(ctx, wcaid, user, isuser)):
            return
        # else, we start the lookup.
        data = (await helper.person_lookup(ctx, wcaid))
        if data is None:
            return
        # checks to see if the user has a WCA ID already set (or "No ID")
        # then edits nickname accordingly :)
        if re.match(" | [1-2][09][8012][0-9][A-Z]{4}[0-9]{2}$", user.display_name):
            await user.edit(nick=(user.display_name[:-13] + " | " + wcaid))
        else:
            await user.edit(nick=(user.display_name + " | " + wcaid))
        # success!
        firstname = data["person"]["name"].split(" ")[0]
        if isuser:
            await ctx.send(f"Your WCA ID has been updated.\nThanks {firstname}!")
        else:
            await ctx.send(f"{firstname}'s WCA ID updated.")
        return

    @commands.command(pass_context=True)
    async def nick(self, ctx, nick, user: discord.Member = ''):
        # checks to see if the user was passed and if the author has permissions
        if (await helper.check_nick_perms(ctx)) and user != '':
            return
        # sets a flag to determine if we are updating the author or another user
        # sets user equal to the author if one was not passed.
        user, isuser = helper.is_user_check(ctx, user)
        # checks if the current nick is the same as what was passed
        if nick == user.display_name[-13]:
            if isuser:
                await ctx.send("Your nickname is already set.")
            else:
                await ctx.send("Nickname already set.")
            return
        # nicknames must not have a vertical bar
        if (await helper.nick_bar_check(ctx, nick, isuser)):
            return
        # just look up the user in WCA to return their first name in the confirmation message
        response = requests.get(cl.WCA_API().persons(wcaid))
        await user.edit(nick=(nick + user.display_name[-13:]))
        if response:
            data = response.json()
            firstname = data["person"]["name"].split(" ")[0]
            if isuser:
                await ctx.send(f"Your nickname has been updated.\nThanks {firstname}!")
            else:
                await ctx.send(f"{firstname}'s nickname updated.")
        else:
            if isuser:
                await ctx.send("Your nickname has been updated. Thanks!")
            else:
                await ctx.send("Nickname updated.")

def setup(client):
    client.add_cog(nickwcaid(client))
