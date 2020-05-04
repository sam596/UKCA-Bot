import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re
import requests
import json
from pyTwistyScrambler import scrambler333
from country_converter import CountryConverter as cc
from datetime import datetime, date
from typing import Union
from events import events, eventids
from format_result import format_result
from wca_format_date import wcadateformat
import webhook

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?')
bot.remove_command("help")

@bot.command()
async def ping(ctx, user: Union[discord.Member, str]):
    await ctx.send(type(user))

@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    embed.set_author(name="Help")
    embed.add_field(
        name = "?nickwcaid <nick> <wca_id>",
        value = "Change your nickname and WCA ID. If your nick is more than one word, encapsulate it in double quotes (\"\"). If you do not have a WCA ID, use \"No ID\" as your wca_id",
        inline = False
    )
    embed.add_field(
        name = "?wcaid <wca_id>",
        value = "Change your WCA ID only.",
        inline = False
    )
    embed.add_field(
        name = "?nick <nick>",
        value = "Change your nick only. If your nick is more than one word, use double quotes (\"\").",
        inline = False
    )
    embed.add_field(
        name = "?personstats <wca_id/user>",
        value = "Returns WCA Stats about the WCA ID or user you tagged. If you didn't write a WCA ID or tag anyone, it returns stats on you!.",
        inline = False
    )
    embed.add_field(
        name = "?ukcomps",
        value = "Returns a list of upcoming competitions in the UK.",
        inline = False
    )
    embed.add_field(
        name = "?pr <event> <wca_id/user>",
        value = "Returns the PRs of the WCA ID or user you tagged for the event you specify. If you didn't write a WCA ID or tag anyone, it returns your own PRs",
        inline = False
    )
    embed.add_field(
        name = "?s <event> <num>",
        value = "Generates <num> TNoodle scrambles for that event. If <num> is not given, it generates one only. If <event> is not given as well, it defaults to one single 3x3 scramble",
        inline = False
    )

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def nickwcaid(ctx, nick, wcaid, user: discord.Member = ''):
    # lists the users roles to check if moderator.
    userroles = []
    for r in ctx.message.author.roles:
        userroles.append(r.id)
    # if the user has specified a user to change and they are not a moderator.
    if user != '' and MODROLEID not in userroles:
        await ctx.send("You do not have the required permission.")
    elif wcaid == '1337MUMG69':
        await ctx.send("wow... so original...")
    elif (user == '' and ctx.message.author.id == ctx.message.guild.owner_id):
        await ctx.send("Sorry, I can't edit the owner of the server.")
    else:
        # ensures we update the correct user
        if user == '':
            user = ctx.message.author
            isuser = True
        else:
            isuser = False
        # checks if the nick and wcaid are different to current display_name
        if nick + " | " + wcaid == user.display_name:
            if isuser:
                await ctx.send("Your nickname and WCA ID is already set.")
            else:
                await ctx.send("Nickname and WCA ID already set.")
        # checks if the nick has a vertical bar
        elif nick.find("|") != -1:
            if isuser:
                await ctx.send("Your nickname must not include a | character")
            else:
                await ctx.send("Nickname must not include a | character")
        # regex to match valid WCA ID before querying API
        elif re.match("[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", wcaid):
            # API query
            response = requests.get(WCA_API_persons + wcaid)
            if response:
                data = response.json()
                # edits user
                await user.edit(nick=(nick + " | " + wcaid))
                if isuser:
                    await ctx.send("Your nickname and WCA ID have been updated.\nThanks " + data["person"]["name"].split(" ")[0] + "!")
                else:
                    await ctx.send(data["person"]["name"].split(" ")[0] + "'s name and WCA ID updated.")
            # 404 implies that the page, and therefore the WCA ID, doesn't exist.
            elif response.status_code == 404:
                await ctx.send("WCA ID " + wcaid + " does not exist.")
            # otherwise there's another error that is not fixable by the user, so tags me.
            else:
                await ctx.send("HTTP Error " + response.status_code + ". WCA might be down, tagging <@169966391758290944> for fix")
        # users can specify No ID
        elif wcaid == "No ID":
            await user.edit(nick=(nick + " | No ID"))
            if isuser:
                await ctx.send("Your nickname has been updated")
            else:
                await ctx.send("Nickname updated")
        # otherwise the WCA ID is not valid
        else:
            await ctx.send(wcaid + " is not a valid WCA ID. Pass !nickwcaid a nickname, followed by a valid WCA ID or \"No ID\"")

@bot.command(pass_context=True)
async def wcaid(ctx, wcaid, user: discord.Member = ''):
    # lists the users roles to check if moderator.
    userroles = []
    for r in ctx.message.author.roles:
        userroles.append(r.id)
    # if the user has specified a user to change and they are not a moderator.
    if user != '' and MODROLEID not in userroles:
        await ctx.send("You do not have the required permission.")
    elif (user == '' and ctx.message.author.id == ctx.message.guild.owner_id):
        await ctx.send("Sorry, I can't edit the owner of the server.")
    else:
        # ensures we update the correct user
        if user == '':
            user = ctx.message.author
            isuser = True
        else:
            isuser = False
        # checks if the WCA ID is already set.
        if user.display_name.find(" | " + wcaid) != -1:
            if isuser:
                await ctx.send("Your WCA ID is already set.")
            else:
                await ctx.send("WCA ID already set.")
        elif user.display_name.find("|") != -1:
            await ctx.send("Please use ?nickwcaid")
        # regex to match valid WCA ID before querying WCA API
        elif re.match("[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", wcaid):
            # api query
            response = requests.get(WCA_API_persons + wcaid)
            if response:
                data = response.json()
                # checks if current display_name has a valid WCA ID/No ID or not...
                if re.match(" | [1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", user.display_name):
                    await user.edit(nick=(user.display_name[:-13] + " | " + wcaid))
                elif user.display_name[:-8] == " | No ID":
                    await user.edit(nick=(user.display_name[:-5] + wcaid))
                else:
                    await user.edit(nick=(user.display_name + " | " + wcaid))
                if isuser:
                    await ctx.send("Your WCA ID has been updated.\nThanks " + data["person"]["name"].split(" ")[0] + "!")
                else:
                    await ctx.send(data["person"]["name"].split(" ")[0] + "'s WCA ID updated.")
            # 404 implies that the page, and therefore the WCA ID, doesn't exist.
            elif response.status_code == 404:
                await ctx.send("WCA ID " + wcaid + " does not exist.")
            # otherwise there's another error that is not fixable by the user, so tags me.
            else:
                await ctx.send("HTTP Error " + response.status_code + ". WCA might be down, tagging <@169966391758290944> for fix")
        # users can say they don't have an ID
        elif wcaid == "No ID":
            # checks if current display_name has a valid WCA ID (i.e. they are anonymising their account).
            if re.match(" | [1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", user.display_name):
                await user.edit(nick=(user.display_name[:-13] + " | No ID"))
            else:
                await user.edit(nick=(user.display_name + " | No ID"))
        # otherwise, it's not a valid WCA ID.
        else:
            await ctx.send(wcaid + " is not a valid WCA ID. Pass !wcaid a valid WCA ID or \"No ID\"")

@bot.command(pass_context=True)
async def nick(ctx, nick, user: discord.Member = ''):
    # lists the users roles to check if moderator.
    userroles = []
    for r in ctx.message.author.roles:
        userroles.append(r.id)
    # if the user has specified a user to change and they are not a moderator.
    if user != '' and MODROLEID not in userroles:
        await ctx.send("You do not have the required permission.")
    elif (user == '' and ctx.message.author.id == ctx.message.guild.owner_id):
        await ctx.send("Sorry, I can't edit the owner of the server.")
    else:
        # ensures we update the correct user
        if user == '':
            user = ctx.message.author
            isuser = True
        else:
            isuser = False
        # checks if the nick and wcaid are different to current display_name
        if nick == user.display_name[-13:]:
            if isuser:
                await ctx.send("Your nickname and WCA ID is already set.")
            else:
                await ctx.send("Nickname and WCA ID already set.")
        # checks if the nick has a vertical bar
        elif nick.find("|") != -1:
            if isuser:
                await ctx.send("Your nickname must not include a | character")
            else:
                await ctx.send("Nickname must not include a | character")
        response = requests.get(WCA_API_persons + user.display_name[-10:])
        await user.edit(nick=(nick + user.display_name[-13:]))
        if response:
            data = response.json()
            await ctx.send("Your nickname has been updated.\nThanks " + data["person"]["name"].split(" ")[0] + "!")
        else:
            await ctx.send("Your nickname has been updated. Thanks!")


@bot.command()
async def personstats(ctx, user: Union[discord.Member, str] = ''):
    if user == '':
        if not re.match("[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", ctx.message.author.display_name[-10:]):
            await ctx.send("As you do not have a WCA ID assigned, you must specify a discord member or WCA ID.")
        else:
            wcaid = ctx.message.author.display_name[-10:]
    elif isinstance(user, str):
        wcaid = user
    else:
        wcaid = user.display_name[-10:]
    if re.match("[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", wcaid):
        response = requests.get(WCA_API_persons + wcaid)
        if response:
            data = response.json()
            embed = discord.Embed(
                title = data["person"]["name"],
                description = cc.convert(data["person"]["country_iso2"],to='name_short'),
                url = data["person"]["url"]
            )
            embed.set_thumbnail(url=data["person"]["avatar"]["url"])
            embed.add_field(name="Competitions", value="**" + str(data["competition_count"]) + "**", inline = False)
            embed.add_field(name="Podiums", value="**" + str(data["medals"]["total"]) + "** - (Gold: " + str(data["medals"]["gold"]) + " Silver: " + str(data["medals"]["silver"]) + " Bronze: " + str(data["medals"]["bronze"]) + ")", inline = False)
            embed.add_field(name="Records", value="**" + str(data["records"]["total"]) + "** - (World: " + str(data["records"]["world"]) + " Continental: " + str(data["records"]["continental"]) + " National: " + str(data["records"]["national"]) + ")", inline = False)
            embed.add_field(name="Completed Solves", value="*TODO*", inline = False)
            if data["person"]["delegate_status"] != None:
                embed.add_field(name="Delegate Status", value=data["person"]["delegate_status"], inline = False)
            if data["person"]["teams"] != []:
                teamlist = ''
                for item in data["person"]["teams"]:
                    teamlist += item["friendly_id"].upper()
                    teamlist += ", "
                teamlist = teamlist[:-2]
                embed.add_field(name="WCA Teams", value=teamlist, inline = False)
            embed.set_footer(text="Data from WCA API (http://www.worldcubeassociation.org/API/v0)")

            await ctx.send(embed=embed)
        elif response.status_code == 404:
            await ctx.send("WCA ID " + wcaid + " does not exist.")
        else:
            await ctx.send("Error " + response.status_code + ". WCA might be down, tagging <@169966391758290944> for fix")
    elif wcaid[-5:] == "No ID":
        await ctx.send("That user does not have a WCA ID assigned.")
    else:
        await ctx.send(wcaid + " is not a valid WCA ID")

@bot.command()
async def ukcomps(ctx):
    response = requests.get(WCA_API_GB_competitions+date.today().isoformat())
    if response:
        data = response.json()
        #embeds = discord.Embed(
        #    title = "Upcoming UK Competitions",
        #    url = "https://www.worldcubeassociation.org/competitions?utf8=%E2%9C%93&region=United+Kingdom&search=&state=present&year=all+years&from_date=&to_date=&delegate=&display=list"
        #)
        for comp in reversed(data):
            embed = discord.Embed(title=comp["name"], description=wcadateformat(comp["start_date"], comp["end_date"]), url=comp["url"])
            embed.set_thumbnail(url="https://i.imgur.com/LMAmWOD.png")
            await ctx.send(embed=embed)

        #compstr = ''
        #for comp in reversed(data):
        #    #competition name
        #    compstr += "**" + comp["name"] + "**\n"
        #    #competition date
        #    sd = datetime.strptime(comp["start_date"], '%Y-%m-%d')
        #    ed = datetime.strptime(comp["end_date"], '%Y-%m-%d')
        #    if sd == ed:
        #        sd = sd.__format__('%B %#d')
        #        compstr += "**" + sd + "**\n"
        #    else:
        #        if sd.__format__('%m') == ed.__format__('%m'):
        #            ed = ed.__format__('%#d')
        #        else:
        #            ed = ed.__format__('%B %#d')
        #        sd = sd.__format__('%B %#d')
        #        compstr += "**" + sd + " - " + ed +"**\n"
        #    #competition location
        #    compstr += comp["city"] + "\n\n"
        #await ctx.send(compstr)
    else:
        await ctx.send("error")

@bot.command()
async def pr(ctx, event, user: Union[discord.Member, str] = ''):
    if user == '':
        if not re.match("[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", ctx.message.author.display_name[-10:]):
            await ctx.send("As you do not have a WCA ID assigned, you must specify a discord member or WCA ID.")
        else:
            wcaid = ctx.message.author.display_name[-10:]
    elif isinstance(user, str):
        wcaid = user
    else:
        wcaid = user.display_name[-10:]
    if re.match("[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}", wcaid):
        event = event.lower()
        for item in events:
            if event in events[item]:
                event = item
        response = requests.get(WCA_API_persons + wcaid)
        if response:
            data = response.json()
            sgl = ""
            avg = "\nAverage: "
            ismbld = "s"
            try:
                sgl += format_result(data["personal_records"][event]["single"]["best"], event, 's')
            except:
                await ctx.send("```No results```")
            try:
                avg += format_result(data["personal_records"][event]["average"]["best"], event, 'a')
                avg += "```"
            except:
                if event != '333mbf':
                    avg = "\nAverage: n/a```"
                else:
                    avg = "```"
                    ismbld = ""
            if sgl != '':
                await ctx.send("```" + data["person"]["name"] + " " + eventids[event] + " Personal Record" + ismbld + "\nSingle: " + sgl + avg)
    elif wcaid[-5:] == "No ID":
        await ctx.send("That user does not have a WCA ID assigned.")
    else:
        await ctx.send(wcaid + " is not a valid WCA ID")

@bot.command()
async def s(ctx, event: str, num=1):
    event = event.lower()
    isevent = False
    for item in events:
        if event in events[item]:
            event = item
            isevent = True
    if num > 5:
        await ctx.send("You cannot generate more than 5 scrambles at a time")
    elif isevent:
        if event[-2:] == "bf":
            event = event[:-2] + "bld"
        response = requests.get(SCRAMBLE_API + event + SCRAMBLE_NUM + str(num))
        data = response.json()
        strsend = "```"
        for i in data["scrambles"]:
            strsend += str(i) + "\n\n"
        strsend += "```"
        await ctx.send(strsend)
    else:
        await ctx.send("Could not match " + event + " to an event.")

@bot.command()
async def clear(ctx, num=1):
    userroles = []
    for r in ctx.message.author.roles:
        userroles.append(r.id)
    # if the user has specified a user to change and they are not a moderator.
    if MODROLEID not in userroles:
        await ctx.send("You do not have the required permission.")
    num = int(num)
    msg = await ctx.channel.history(limit=num+1).flatten()
    await ctx.channel.delete_messages(msg)

bot.run(TOKEN)
