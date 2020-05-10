import requests
from datetime import date, datetime
import time
import discord
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import tasks
from cogs.lib.events_dict import eventids
from cogs.lib.wca_format_date import wcadateformat
from os import getenv as envv
from dotenv import load_dotenv
load_dotenv()


webhook = Webhook.from_url(envv("WEBHOOK_URL"), adapter=RequestsWebhookAdapter())

WCA_API_persons = envv("STAGING_WCA_API") + "persons/"
WCA_API_upcoming_GB = envv("STAGING_WCA_API") + "competitions?page=1&country_iso2=GB&start=" + date.today().isoformat()
WCA_API_upcoming_XE = envv("STAGING_WCA_API") + "competitions?country_iso2=XE&start=" + date.today().isoformat()
WCA_API_upcoming_WC = envv("STAGING_WCA_API") + "search/competitions?q=WCA%20World&start=" + date.today().isoformat()
WCA_API_upcoming_EC = envv("STAGING_WCA_API") + "search/competitions?q=WCA%20Euro&start=" + date.today().isoformat()

@tasks.loop(seconds=10)
async def testing():
    webhook.send("testing")


@tasks.loop(minutes=5)
async def comp_announcements():
    with open("complist.txt") as f:
        complist = f.read().splitlines()
    compsjson = []
    for param in ("GB", "XE"):
        exec("response_" + param + " = requests.get(WCA_API_upcoming_" + param + ")")
        exec("data_" + param + " = response_" + param + ".json()")
        exec("for i in data_" + param + ":\n    compsjson.append(i)")

    for param in ("WC", "EC"):
        exec("response_" + param + " = requests.get(WCA_API_upcoming_" + param + ")")
        exec("data_" + param + " = response_" + param + ".json()")
        exec("for i in data_" + param + "[\"result\"]:\n    compsjson.append(i)")

    for comp in compsjson:
        if comp["id"] not in complist:
            complist.append(comp["id"])
            with open("complist.txt", 'a') as f:
                f.write(comp["id"]+"\n")
            eventlist = ''

            for eventid in eventids:
                if eventid in comp["event_ids"]:
                    eventlist += eventids[eventid][1] + ", "

            eventlist = eventlist[:-2]

            regopen = datetime.strptime(comp["registration_open"], "%Y-%m-%dT%H:%M:%S.%fZ")
            embed = discord.Embed(
                title=comp["name"],
                description=wcadateformat(comp["start_date"], comp["end_date"]),
                url=comp["url"]
            )
            embed.add_field(name="City", value=comp["city"])
            embed.add_field(name="Registration Opens", value=datetime.strftime(regopen, "%d/%m/%y %H:%M"))
            embed.add_field(name="Competitor Limit", value=comp["competitor_limit"])
            embed.add_field(name="Events", value=eventlist)
            embed.set_thumnail(url="https://i.imgur.com/LMAmWOD.png")
            webhook.send("**" + comp["name"] + "** has been announced!", embed=embed)
