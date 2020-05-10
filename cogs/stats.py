import discord
import os
from discord.ext import commands
import requests
from .lib import helpers as helper, wca_format_date as wfd, cr_dict
from .lib.classes import WCA_API
from typing import Union


class stats(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def personstats(self, ctx, user: Union[discord.Member, str] = ''):
        # sets user = author if none was passed
        user, isuser = helper.is_user_check(ctx, user)
        wcaidinvalid, wcaid = (await helper.wcaid_validity_stats(ctx, user, isuser))
        if wcaidinvalid:
            return
        data = (await helper.person_lookup(ctx, wcaid))
        if data is None:
            return
        embed = helper.build_personstats_embed(data)
        await ctx.send(embed=embed)

    @commands.command()
    async def ukcomps(self, ctx):
        response = requests.get(WCA_API().upcoming("GB"))
        if response:
            data = response.json()
            for comp in reversed(data):
                embed = discord.Embed(title=comp["name"], description=wfd.wcadateformat(comp["start_date"], comp["end_date"]), url=comp["url"])
                embed.set_thumbnail(url="https://i.imgur.com/LMAmWOD.png")
                await ctx.send(embed=embed)
        else:
            await ctx.send("error")

    @commands.command(pass_context=True)
    async def pr(self, ctx, event: str, user: Union[discord.Member, str] = ''):
        user, isuser = helper.is_user_check(ctx, user)
        wcaidinvalid, wcaid = (await helper.wcaid_validity_stats(ctx, user, isuser))
        eventcheck = (await helper.event_check(ctx, event))
        if wcaidinvalid or eventcheck[0]:
            return
        event = eventcheck[1]
        data = (await helper.person_lookup(ctx, wcaid))
        if data is None:
            return
        await ctx.send(helper.build_prs_codeblock(data, event))

    @commands.command()
    async def nr(self, ctx, country = 'GB', event = ''):
        countryiso2 = helper.country_lookup_iso2(ctx, country)
        if countryiso2 == 'not found':
            await ctx.send(f"Could not match {country} to a valid country")
            return
        if event != '':
            eventcheck = (await helper.event_check(ctx, event))
            if eventcheck[0]:
                return
            event = eventcheck[1]
        recordlookup = (await helper.get_nat_records(ctx, countryiso2))
        if recordlookup[0]:
            return
        if event == '':
            record_string = (await helper.all_events_records_print(ctx, recordlookup[1]))
            await ctx.send(f"```{recordlookup[2]} National Records\n\n{record_string}```")
        else:
            found, record_string, readable_event = (await helper.sgl_event_record_print(ctx, recordlookup[1], event))
            if found:
                await ctx.send(f"```{recordlookup[2]} {readable_event} National Records\n\n{record_string}```")
        return

    @commands.command()
    async def cr(self, ctx, cont = 'Europe', event = ''):
        iscont = False
        cont = cont.lower()
        for continent in cr_dict.continents:
            if cont in cr_dict.continents[continent]:
                cont = continent
                iscont = True
                break
        if not iscont:
            await ctx.send(f"Could not match {cont} to a valid continent")
            return
        if event != '':
            eventcheck = (await helper.event_check(ctx, event))
            if eventcheck[0]:
                return
            event = eventcheck[1]
        recordlookup = (await helper.get_cont_records(ctx, cont))
        if recordlookup[0]:
            return
        if event == '':
            record_string = (await helper.all_events_records_print(ctx, recordlookup[1]))
            await ctx.send(f"```{cr_dict.continents[cont][-1]} Records\n\n{record_string}```")
        else:
            found, record_string, readable_event = (await helper.sgl_event_record_print(ctx, recordlookup[1], event))
            if found:
                await ctx.send(f"```{cr_dict.continents[cont][-1]} {readable_event} Records\n\n{record_string}```")
        return

    @commands.command()
    async def wr(self, ctx, event = ''):
        if event != '':
            eventcheck = (await helper.event_check(ctx, event))
            if eventcheck[0]:
                return
            event = eventcheck[1]
        recordlookup = (await helper.get_world_records(ctx))
        if recordlookup[0]:
            return
        if event == '':
            record_string = (await helper.all_events_records_print(ctx, recordlookup[1]))
            await ctx.send(f"```World Records\n\n{record_string}```")
        else:
            found, record_string, readable_event = (await helper.sgl_event_record_print(ctx, recordlookup[1], event))
            if found:
                await ctx.send(f"```World {readable_event} Records\n\n{record_string}```")
        return




def setup(client):
    client.add_cog(stats(client))
