import discord
import asyncio
import re
import requests
from textwrap import dedent
from . import classes as cl, events_dict
from .format_result import format_result as fr
import country_converter as coco


def wcaid_re(wcaid):
    if re.match("^[1-2][09][8012][0-9][A-Z]{4}[0-9]{2}$", wcaid):
        return True
    else:
        return False

async def check_nick_perms(ctx):
    # author needs manage nicknames
    if not ctx.message.author.permissions_in(ctx.channel).manage_nicknames:
        await ctx.send("You do not have the required permission to manage nicknames.")
        return True
    # author cannot be the owner
    elif ctx.message.author.id == ctx.message.guild.owner_id:
        await ctx.send("Sorry, I can't edit the owner of the server.")
        return True
    else:
        return False

def is_user_check(ctx, user):
    # self explanatory
    if user == '':
        user = ctx.message.author
        isuser = True
    else:
        isuser = False
    return user, isuser

async def nick_bar_check(ctx, nick, isuser):
    # vertical bar needs to be absent from nick
    if nick.find("|") != -1:
        if isuser:
            await ctx.send("Your nickname must not include a | character.")
        else:
            await ctx.send("Nickname must not include a | character.")
        return True
    else:
        return False

async def no_id_check(ctx, wcaid, isuser, ):
    if re.match("^NO( |)ID$", wcaid):
        if isuser:
            await ctx.send("Your nickname has been updated")
        else:
            await ctx.send("Nickname updated")
        return True
    return False

async def wcaid_validity_nick(ctx, wcaid, user, isuser):
    # regex for a potentially valid WCA ID (until 2030 mind you)
    if wcaid_re(wcaid):
        return False
    else:
        await ctx.send(wcaid + " is not a valid WCA ID. Pass a valid WCA ID or \"No ID\"")
        return True

async def wcaid_validity_stats(ctx, user, isuser):
    if isinstance(user, str):
        wcaid = user.upper()
        if not wcaid_re(wcaid):
            await ctx.send(f"{wcaid} is not a valid WCA ID.")
            return True, ''
    else:
        wcaid = user.display_name[-10:]
        if not wcaid_re(wcaid):
            if isuser:
                await ctx.send("You do not have a WCA ID assigned, use ?wcaid or ?nickwcaid to assign your WCA ID")
            else:
                await ctx.send("That user does not have a WCA ID assigned")
            return True, ''
    return False, wcaid


async def person_lookup(ctx, wcaid):
    # queries API for the WCA ID given.
    response = requests.get(cl.WCA_API().persons(wcaid))
    # if 404, that WCA ID doesn't exist
    if response.status_code == 404:
        await ctx.send(f"WCA ID {wcaid} does not exist")
        return None
    # if there's another error, oops!
    try:
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        await ctx.send(f"Sorry, an error occurred.\n{e}")
        return None
    # return the json in dict form.
    return response.json()

def build_personstats_embed(data):
    cc = coco.CountryConverter()
    embed = discord.Embed(
        title = data["person"]["name"],
        description = cc.convert(names=data["person"]["country_iso2"],to='name_short'),
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
    return embed

async def event_check(ctx, event):
    event = event.lower()
    isevent = False
    for item in events_dict.events:
        if event in events_dict.events[item]:
            event = item
            isevent = True
    if not isevent:
        await ctx.send(f"Could not match {event} to a WCA event.")
        return True, ''
    return False, event

def build_prs_codeblock(data, event):
    try:
        single = data["personal_records"][event]["single"]["best"]
    except KeyError:
        return "``` No Results ```"

    try:
        average = data["personal_records"][event]["average"]["best"]
    except KeyError:
        average = 0

    single = fr(single, event, 's')
    average = fr(average, event, 'a')

    if average == '':
        average = "Not Achieved."

    if event == "333mbf":
        ismbld = True
        average = ''
        plural_s = ''
    else:
        ismbld = False
        average = f"Average: {average}"
        plural_s = 's'

    name = data["person"]["name"]
    event = events_dict.eventids[event][0]

    result = f"""\
    ```
    {name}'s {event} Personal Record{plural_s}
    Single: {single}
    {average}```"""

    return dedent(result)

def country_lookup_iso2(ctx, country):
    if country.upper() == 'UK':
        return 'GB'
    cc = coco.CountryConverter()
    country = cc.convert(names=country,to='ISO2')
    return country

async def get_nat_records(ctx, countryiso2):
    response = requests.get(cl.WCA_API().recordslookup())

    try:
        response.raise_for_status()
    except:
        await ctx.send("Sorry, an error occurred. Try again later.")
        return True, '', ''

    data = response.json()
    cc = coco.CountryConverter()

    wcacountry = ''

    for country in data["national_records"]:
        if cc.convert(names=country,to='ISO2') == countryiso2:
            wcacountry = country
            break

    if wcacountry == '':
        await ctx.send(f"Sorry, I matched your input to {cc.convert(names=countryiso2,to='name_short')} but I couldn't find that country in the WCA. If you believe this to be an error, contact Sam.")
        return True, '', ''

    return False, data["national_records"][wcacountry], cc.convert(names=countryiso2,to='name_short')

def ordered_event_list(table):
    eventlist = []
    for eventid in events_dict.eventids:
        for key in table:
            if key == eventid:
                eventlist.append(key)
    return eventlist

async def all_events_records_print(ctx, table):
    record_string = ''
    eventlist = ordered_event_list(table)
    for event in eventlist:
        try:
            average_string = f" - Average: {fr(table[event]['average'], event, 'a')}"
        except KeyError:
            average_string = ''
        record_string += f"{events_dict.eventids[event][0]} --- Single: {fr(table[event]['single'], event, 's')}{average_string}\n"
    return record_string

async def sgl_event_record_print(ctx, table, event):
    try:
        single = fr(table[event]["single"], event, "s")
    except KeyError:
        ctx.send("```No results```")
        return False, '', ''
    try:
        average_string = f" - Average: {fr(table[event]['average'], event, 'a')}"
    except KeyError:
        average_string = ''
    record_string = f"Single: {single}{average_string}"
    return True, record_string, events_dict.eventids[event][0]

async def get_cont_records(ctx, continent):
    response = requests.get(cl.WCA_API().recordslookup())

    try:
        response.raise_for_status()
    except:
        await ctx.send("Sorry, an error occurred. Try again later.")
        return True, '', ''

    data = response.json()

    return False, data["continental_records"][continent]

async def get_world_records(ctx):
    response = requests.get(cl.WCA_API().recordslookup())

    try:
        response.raise_for_status()
    except:
        await ctx.send("Sorry, an error occurred. Try again later.")
        return True, '', ''

    data = response.json()

    return False, data["world_records"]
