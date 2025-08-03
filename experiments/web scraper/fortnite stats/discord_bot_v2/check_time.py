import datetime
import discord
from discord.ext import tasks
import csv

TOKEN = ''
FNShopDate_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\FNShopDate.csv"
client = discord.Client(intents = discord.Intents.all())

print(datetime.datetime.now())

@tasks.loop(seconds=1) #Create the task
async def Check_shop():
    try:
        f = open(FNShopDate_path)
    except:
        pass
    else:
        today = datetime.datetime.now()
        today = today - datetime.timedelta(hours=1)
        today = today.strftime('%d-%m-%Y')
        date = []
        date.append(today)
        with open(FNShopDate_path, 'r', newline='') as file:
            csvreader = csv.reader(file)
            if next(csvreader) == date:
                channel = client.get_channel(1241269194755145770)
                await channel.send("test1")
            else:
                channel = client.get_channel(1241269194755145770)
                await channel.send("test2")

@client.event
async def on_ready():
    if not Check_shop.is_running():
        Check_shop.start() #If the task is not already running, start it.
        print("Check Shop task started")

client.run(TOKEN)
