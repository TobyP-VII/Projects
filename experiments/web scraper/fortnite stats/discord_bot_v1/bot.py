import discord
import responses
import requests
import json

stats_list = []
account_name_list = ["Account Name: "]
overall_wins_list = ["Overall Wins: "]
solo_wins_list = ["solo Wins: "]
duo_wins_list = ["Duo Wins: "]
squad_wins_list = ["Squad Wins: "]

def get_stats(account_name):
  url = "https://fortnite-api.com/v2/stats/br/v2?name=" + account_name + "&timeWindow=season&accountType=epic"

  payload = {}
  headers = {
    'Authorization': 'c128fa59-591f-4815-85ff-8ed3727694da'
  }

  response = requests.request("GET", url, headers=headers, data=payload)
  if (str(response) == "<Response [404]>"):
    responses.stats_list = ("No account found with the name: " + str(account_name))
    url = "https://fortnite-api.com/v2/stats/br/v2?name=" + account_name + "&timeWindow=season&accountType=xbl"

    payload = {}
    headers = {
      'Authorization': 'c128fa59-591f-4815-85ff-8ed3727694da'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if (str(response) == "<Response [404]>"):
      responses.stats_list = ("No account found with the name: " + str(account_name))
      url = "https://fortnite-api.com/v2/stats/br/v2?name=" + account_name + "&timeWindow=season&accountType=psn"

      payload = {}
      headers = {
        'Authorization': 'c128fa59-591f-4815-85ff-8ed3727694da'
      }

      response = requests.request("GET", url, headers=headers, data=payload)
      if (str(response) == "<Response [404]>"):
        responses.stats_list = ("No account found with the name: " + str(account_name))
        print("\033[0;31;48m\nNo account found with that name... \033[0m")
      else:
        set_stats(response.text, account_name)
    else:
      set_stats(response.text, account_name)
  else:
    set_stats(response.text, account_name)

def set_stats(response, account_name):
  response_data = json.loads(response)
  try:
    overall_wins = (response_data['data']['stats']['all']['overall']['wins'])
  except:
    overall_wins = ("NO DATA")
  try:
    solo_wins = (response_data['data']['stats']['all']['solo']['wins'])
  except:
    solo_wins = ("NO DATA")
  try:
    duo_wins = (response_data['data']['stats']['all']['duo']['wins'])
  except:
    duo_wins = ("NO DATA")
  try:
    squad_wins = (response_data['data']['stats']['all']['squad']['wins'])
  except:
    squad_wins = ("NO DATA")

  account_name_list.append(account_name)
  overall_wins_list.append(overall_wins)
  solo_wins_list.append(solo_wins)
  duo_wins_list.append(duo_wins)
  squad_wins_list.append(squad_wins)

  stats_list = ([account_name_list, overall_wins_list, solo_wins_list, duo_wins_list, squad_wins_list])
  responses.stats_list = str("CURRENT SEASON\nAccount Name: " + str(account_name) + "\n" + "Overall Wins: " + str(overall_wins) + "\n" + "Solo Wins: " + str(solo_wins) + "\n" + "Duo Wins: " + str(duo_wins) + "\n" + "Squad Wins: " + str(squad_wins))
  for x in range(1, len(account_name_list)):
    print("\n")
    for i in range(0, len(stats_list)):
      print("\033[1;34;48m" + str(stats_list[i][0]) + "\033[0;32;48m" + str(stats_list[i][x]) + "\033[0m")

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]

            get_stats(user_message)

            await send_message(message, user_message, is_private = False)
        else:
            pass

    client.run(TOKEN)
