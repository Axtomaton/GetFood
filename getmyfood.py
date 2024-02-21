import discord
from bs4 import BeautifulSoup
from discord.ext import commands
import requests
from dataclasses import dataclass
import datetime
import argparse 
from tabulate import tabulate
from table2ascii import table2ascii as t2a, PresetStyle

parser = parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--BotToken',
                    help='Please visit `https://discord.com/developers/applications` to get your bot token')
parser.add_argument('--ChannelID',
                    help='Please visit `https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-` to get your channel id')
args = parser.parse_args()

BOT_TOKEN = args.BotToken
CHANNEL_ID = args.ChannelID
print(args.BotToken)
print(args.ChannelID)


##-------------GLOBAL VARIABLES

URL = "https://www.rit.edu/fa/diningservices/"
CHANNEL_ID = 1206785484341248010

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@dataclass 
class Session: 
    is_active: bool = False
    start_time: int = 0

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()

@bot.event
async def on_ready():
    print("Hello! RIT Food bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello! Study bot is ready!")


@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f"New session started at {human_readable_time}")

@bot.command()
async def food(ctx):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    food_and_time = [data.get_text().strip() for data in soup.find_all("div", class_="visitingchef-event")]

    foods = []
    times = []
    for info in food_and_time:
        i = 0
        l = len(info)
        while i < l and not info[i].isdigit():
            i += 1

        if i < l:
            food, time = info[:i - 1], info[i:]
            time = time.strip()
            food = food.strip()
            time = time.lstrip("(")
            time = time.rstrip(")")
            if not time:
                time = "N/A"
        else:
            food = info
            time = "N/A"
        foods.append(food)
        times.append(time)

    locations = [location.get_text().strip() for location in soup.find_all("div", class_="visitingchef-location")]
    headers = ["FOOD", "TIME", "LOCATION"]
    data = list(zip(foods, times, locations))
    output = t2a (
        header = headers,
        body   = data,
        style  = PresetStyle.thin_compact
    )
    await ctx.send("```" + output + "```")
    
@bot.command()
async def end(ctx):
    if not session.is_active:
        await ctx.send("No session is active!")
        return
    session.is_active = False
    end_time = ctx.message.created_at.timestamp()
    duration = end_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    await ctx.send(f"Session ended after {human_readable_duration}.")

if __name__ == "__main__":
    bot.run(BOT_TOKEN)
