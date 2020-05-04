import requests
from datetime import date, datetime
import time
import discord
from discord import Webhook, RequestsWebhookAdapter
from events import eventids
from wca_format_date import wcadateformat
from jsonmerge import merge

webhook_url = "https://discordapp.com/api/webhooks/706529849078186046/0Ublk5p97v49lROomqeiVBaBiuP13jfuaL394baW9jc-RNF_jtjLnDRtHpz9JQKyw509"
webhook = Webhook.from_url(webhook_url, adapter=RequestsWebhookAdapter())

WCA_API = "https://staging.worldcubeassociation.org/api/v0/"
WCA_API_upcoming_GB = WCA_API + "competitions?page=1&country_iso2=GB&start=" + date.today().isoformat()
WCA_API_upcoming_XE = WCA_API + "competitions?country_iso2=XE&start=" + date.today().isoformat()
WCA_API_upcoming_WC = WCA_API + "search/competitions?q=WCA%20World&start=" + date.today().isoformat()
WCA_API_upcoming_EC = WCA_API + "search/competitions?q=WCA%20Euro&start=" + date.today().isoformat()


with open("complist.txt") as f:
    complist = f.read().splitlines()

while True:
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
            f = open("complist.txt", 'a')
            f.write(comp["id"]+"\n")
            f.close()
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
            webhook.send("**" + comp["name"] + "** has been announced!", embed=embed)
    time.sleep(300)
