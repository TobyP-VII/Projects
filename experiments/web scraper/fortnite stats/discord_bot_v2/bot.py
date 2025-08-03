import discord
from check_command import get_stats, get_news, get_map, get_shop
from discord import app_commands
from discord.ext import commands, tasks
import csv
import datetime
import nest_asyncio
nest_asyncio.apply()

def check_date(item_time):
    today = datetime.datetime.now()
    today = today - datetime.timedelta(hours=1)
    today = today.strftime('%d-%m-%Y')
    date = []
    date.append(today)

    if str(date) == str(item_time):
        print("FOUND!!!")
        return(True)
    else:
        return(False)

# discord key
TOKEN = ''
FNNewItems_path = r'C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\FNNewItems.csv'
FNShopDate_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\FNShopDate.csv"
FortniteShop_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\FortniteShop.png"

bot = commands.Bot(command_prefix= '!', intents = discord.Intents.all())

def embed_file(new_items):
    file = discord.File(FortniteShop_path, filename = 'FortniteShop.png')
    embed = discord.Embed(title = 'CURRENT ITEM SHOP', description = (f'NEW ITEMS: {new_items[0]}!'), colour = discord.Color.from_rgb(103, 97, 242))
    embed.set_image(url="attachment://FortniteShop.png")
    embed.set_thumbnail(url = bot.user.avatar.url)
    return(embed, file)

def check_new_items():
    with open(FNNewItems_path, 'r', newline='') as file:
        csvreader = csv.reader(file)
        new_items = next(csvreader)
        print (new_items)
        return new_items
#print when everything is fine and dandy
@bot.event
async def on_ready():
    print("Bot Running")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print (e)

#stats

@bot.tree.command(name="stats")
@app_commands.describe(account_name = "account name", stat = "stat to check", timeframe = "timeframe", platform = "platform")
#takes input from .describe
@app_commands.choices(stat = [
    #must be name = "" and values = ""
    discord.app_commands.Choice(name = 'wins', value = 'wins'),
    discord.app_commands.Choice(name = 'kills', value = 'kills')
])
@app_commands.choices(timeframe = [
    discord.app_commands.Choice(name = 'lifetime', value = 'lifetime'),
    discord.app_commands.Choice(name = 'current season', value = 'season')
])
@app_commands.choices(platform = [
    discord.app_commands.Choice(name = 'epic', value = 'epic'),
    discord.app_commands.Choice(name = 'xbox', value = 'xbl'),
    discord.app_commands.Choice(name = 'playstation', value = 'psn')
])

async def say(interaction: discord.Interaction, account_name: str, stat: discord.app_commands.Choice[str], timeframe: discord.app_commands.Choice[str], platform: discord.app_commands.Choice[str]):
#interaction:discord.Interaction is for receiving the interaction from above command
#variable:discord.app_commands.Choice[] forces that input

    await interaction.response.send_message(
        #sends this as a message
        get_stats(account_name, stat.value, timeframe.value, platform.value, stat.name, timeframe.name, platform.name)
    )

#news

@bot.tree.command(name="news")
async def say(interaction: discord.Interaction):
    
    await interaction.response.send_message(
        get_news()
    )

#map

@bot.tree.command(name="map")
@app_commands.describe(map_type = "map type")
@app_commands.choices(map_type = [
    discord.app_commands.Choice(name = 'with POIs', value = 'pois'),
    discord.app_commands.Choice(name = 'without POIs', value = 'blank')
])
async def say(interaction: discord.Interaction, map_type: discord.app_commands.Choice[str]):
    
    await interaction.response.send_message(
        get_map(map_type.value)
    )

#shop

@bot.tree.command(name="shop")
async def say(interaction: discord.Interaction):


    #get date
    today = datetime.datetime.now()
    #make date 1hr behind due to item shop resetting 1hr later
    today = today - datetime.timedelta(hours=1)
    #output ins d-m-y format, can be any orientation
    today = today.strftime('%d-%m-%Y')
    #make an array to store the date so that it is easily input and read from a csv file
    date = []
    date.append(today)
    #set the file paths as variables so that the file has permissions to open and edit them
    
    try:
        #check if the file exists
        f = open(FNShopDate_path)
    except FileNotFoundError:
        #if file doesn't exist
        #start thinking while creating file
        await interaction.response.defer(thinking=True)
        #get file
        get_shop()
        new_items = check_new_items()
        await interaction.followup.send(
            embed = embed_file(new_items)[0], file = embed_file(new_items)[1]
            )
    else:
        #if file does exist
        try:
        #check if the file exists
            f = open(FortniteShop_path)
        except FileNotFoundError:
            #if file doesn't exist
            #start thinking while creating file
            await interaction.response.defer(thinking=True)
            #get file
            get_shop()
            new_items = check_new_items()
            await interaction.followup.send(
                embed = embed_file(new_items)[0], file = embed_file(new_items)[1]
                )
        else:
            #open file as reader
            with open(FNShopDate_path, 'r', newline='') as file:
                csvreader = csv.reader(file)
                #if what is in file == date
                if next(csvreader) == date:
                    await interaction.response.defer(thinking=True)
                    new_items = check_new_items()
                    await interaction.followup.send(
                        embed = embed_file(new_items)[0], file = embed_file(new_items)[1]
                        )
                else:
                    await interaction.response.defer(thinking=True)
                    get_shop()
                    new_items = check_new_items()
                    await interaction.followup.send(
                        embed = embed_file(new_items)[0], file = embed_file(new_items)[1]
                        )
                    


bot.run(TOKEN)