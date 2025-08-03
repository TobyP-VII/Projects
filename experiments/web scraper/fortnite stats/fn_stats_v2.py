import requests
import json
import keyboard

print("\033[0;31;48m\n███████╗███████╗ █████╗ ███████╗ ██████╗ ███╗   ██╗\n██╔════╝██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║\n███████╗█████╗  ███████║███████╗██║   ██║██╔██╗ ██║\n╚════██║██╔══╝  ██╔══██║╚════██║██║   ██║██║╚██╗██║\n███████║███████╗██║  ██║███████║╚██████╔╝██║ ╚████║\n╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝\n                                                   \n    ███████╗████████╗ █████╗ ████████╗███████╗     \n    ██╔════╝╚══██╔══╝██╔══██╗╚══██╔══╝██╔════╝     \n    ███████╗   ██║   ███████║   ██║   ███████╗     \n    ╚════██║   ██║   ██╔══██║   ██║   ╚════██║     \n    ███████║   ██║   ██║  ██║   ██║   ███████║     \n    ╚══════╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚══════╝     \n                                                   \033[0m \n")

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
    url = "https://fortnite-api.com/v2/stats/br/v2?name=" + account_name + "&timeWindow=season&accountType=xbl"

    payload = {}
    headers = {
      'Authorization': 'c128fa59-591f-4815-85ff-8ed3727694da'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    if (str(response) == "<Response [404]>"):
      url = "https://fortnite-api.com/v2/stats/br/v2?name=" + account_name + "&timeWindow=season&accountType=psn"

      payload = {}
      headers = {
        'Authorization': 'c128fa59-591f-4815-85ff-8ed3727694da'
      }

      response = requests.request("GET", url, headers=headers, data=payload)
      if (str(response) == "<Response [404]>"):
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
  for x in range(1, len(account_name_list)):
    print("\n")
    for i in range(0, len(stats_list)):
      print("\033[1;34;48m" + str(stats_list[i][0]) + "\033[0;32;48m" + str(stats_list[i][x]) + "\033[0m")


while True:
  print("\033[1;34;48m\n")
  account_name_prompt = "Enter an account name"
  account_name_prompt = account_name_prompt.center(51,"-")
  print(account_name_prompt)
  account_name = input("")
  get_stats(account_name)

  if keyboard.is_pressed('del'):
    exit_prompt = "ARE YOU SURE YOU WANT TO EXIT? (Y/N)"
    exit_prompt = exit_prompt.center(51, "-")
    exit_input = input("")
    if exit_input.lower == "y":
      quit()
    else:
      pass
  
