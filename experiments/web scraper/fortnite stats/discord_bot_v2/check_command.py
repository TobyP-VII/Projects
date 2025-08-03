#dealing with commands from bot.py

def get_stats(account_name, stat, timeframe, platform, stat_name, timeframe_name, platform_name):
    #fortnite API key
    FNAPI = 'c128fa59-591f-4815-85ff-8ed3727694da'
    import requests
    import json
    import math
    #get url for use in requests
    #generate custom URL based on inputs
    url = (f"https://fortnite-api.com/v2/stats/br/v2?name={account_name}&timeWindow={timeframe}&accountType={platform}")
    payload = {}
    #authorization is the API key
    headers = {'Authorization': FNAPI}
    #response is the data output as a json file
    response = requests.request("GET", url, headers=headers, data=payload)
    #checks if the response failed or not
    if (str(response) == "<Response [404]>"):
        #if failed it can only mean the name or platform was incorrect
        output_message = (f"No {platform_name} account found with the name: {account_name}")
    else:
        #using the json module, convert the response into a python array
        response_data = json.loads(response.text)
        #check data in array besed on the stat for outputting later
        try:
            solo_stat = (response_data['data']['stats']['all']['solo'][stat])
        except:
            solo_stat = ("0")
        try:
            duo_stat = (response_data['data']['stats']['all']['duo'][stat])
        except:
            duo_stat = ("0")
        try:
            squad_stat = (response_data['data']['stats']['all']['squad'][stat])
        except:
            squad_stat = ("0")

        #use maths to figure out the overall stuff as the overall stat from the API includes LTM
        overall_stat = (int(solo_stat) + int(duo_stat) + int(squad_stat))
        #set output message
        output_message = (f"Found {platform_name} account found with the name: {account_name}\n\n{timeframe_name}\n\nOverall {stat_name}: {overall_stat}\nSolo {stat_name}: {solo_stat}\nDuo {stat_name}: {duo_stat}\nSquad {stat_name}: {squad_stat}")

        #seperately check data for kills to get KD
        if stat == "kills":
            try:
                solo_kd_stat = (response_data['data']['stats']['all']['solo']['kd'])
            except:
                solo_kd_stat = ("0")
            try:
                duo_kd_stat = (response_data['data']['stats']['all']['duo']['kd'])
            except:
                duo_kd_stat = ("0")
            try:
                squad_kd_stat = (response_data['data']['stats']['all']['squad']['kd'])
            except:
                squad_kd_stat = ("0")
            
            overall_kd_stat = math.ceil(((int(solo_kd_stat) + int(duo_kd_stat) + int(squad_kd_stat))/3)*1000)/1000
            #remake output message with KD included
            output_message = (f'Found {platform_name} account found with the name: {account_name}\n\n{timeframe_name}\n\nOverall {stat_name}: {overall_stat} - {"kd"}: {overall_kd_stat}\nSolo {stat_name}: {solo_stat} - {"kd"}: {solo_kd_stat}\nDuo {stat_name}: {duo_stat} - {"kd"}: {duo_kd_stat}\nSquad {stat_name}: {squad_stat} - {"kd"}: {squad_kd_stat}')
        else:
            #do nothing if stat doesn't == kills
            pass

        #do same for wins to get winrate
        if stat == "wins":
            try:
                solo_winRate_stat = (response_data['data']['stats']['all']['solo']['winRate'])
            except:
                solo_winRate_stat = ("0")
            try:
                duo_winRate_stat = (response_data['data']['stats']['all']['duo']['winRate'])
            except:
                duo_winRate_stat = ("0")
            try:
                squad_winRate_stat = (response_data['data']['stats']['all']['squad']['winRate'])
            except:
                squad_winRate_stat = ("0")
            
            overall_winRate_stat = math.ceil(((int(solo_winRate_stat) + int(duo_winRate_stat) + int(squad_winRate_stat))/3)*1000)/1000

            output_message = (f'Found {platform_name} account found with the name: {account_name}\n\n{timeframe_name}\n\nOverall {stat_name}: {overall_stat} - {"winRate"}: {overall_winRate_stat}\nSolo {stat_name}: {solo_stat} - {"winRate"}: {solo_winRate_stat}\nDuo {stat_name}: {duo_stat} - {"winRate"}: {duo_winRate_stat}\nSquad {stat_name}: {squad_stat} - {"winRate"}: {squad_winRate_stat}')
        else:
            pass
    
    #return output message so that bot.py actually gets the data to send
    return output_message

def get_news():
    import requests
    import json

    url = "https://fortnite-api.com/v2/news"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = json.loads(response.text)

    news = (response_data['data']['br']['image'])
    
    output_message = (news)
    
    return (output_message)

def get_map(map_type):
    import requests
    import json
    url = "https://fortnite-api.com/v1/map"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = json.loads(response.text)

    map = (response_data['data']['images'][map_type])
    
    output_message = (map)
    
    return (output_message)

def get_shop():
    import requests
    import json
    from FNShop import get_shop
    from bot import check_date
    import csv

    url = "https://fortnite-api.com/v2/shop/br"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = json.loads(response.text)

    #pre define arrays for later use
    #overall item list
    shop_items = []
    #single item list to put into overall list for easier navigation
    shop_current_item = []
    #dictionary for sorting based on the item type by assorting numbers to them
    item_order = {
        "Bundle": 1,
        "outfit": 2,
        "backpack": 3,
        "pickaxe": 4,
        "glider": 5,
        "emote": 6,
        "wrap": 7,
        "contrail": 8,
        "loadingscreen": 9,
        "music": 10
    }
    new_items = 0

    #loop for everything that are in entries for the item shop
    for x in range (0, len(response_data['data']['featured']['entries'])):
        #set backbling to none to prevent crashing
        backbling_image = 'None'
        #check if the entry  is a bundle or not
        if str(response_data['data']['featured']['entries'][x]['bundle']) != 'None':
            #if entry IS a bundle
            #take out data needed
            item = (response_data['data']['featured']['entries'][x]['bundle']['name'])
            image = (response_data['data']['featured']['entries'][x]['newDisplayAsset']['materialInstances'][0]['images']['Background'])
            layout_id = (response_data['data']['featured']['entries'][x]['layout']['id'])
            item_type = (response_data['data']['featured']['entries'][x]['bundle']['info'])
            section_id = (response_data['data']['featured']['entries'][x]['sectionId'])
            item_type = item_order[str(item_type)]
            price = str(response_data['data']['featured']['entries'][x]['finalPrice'])
            item_yesterdate = 'None'
            shop_current_item = [image, item, layout_id, item_type, backbling_image, section_id, price, item_yesterdate]
            #check if this is already in the list just to make sure theres no duplicates
            if shop_current_item in shop_items:
                pass
            else:
                #add to list
                shop_items.append(shop_current_item)
        else:
            #if entry is NOT a bundle
            try:
                #check for specific data to determin if it's the correct type
                item = (response_data['data']['featured']['entries'][x]['items'][0]['name'])
                image = (response_data['data']['featured']['entries'][x]['newDisplayAsset']['materialInstances'][0]['images']['Background'])
                layout_id = (response_data['data']['featured']['entries'][x]['layout']['id'])
                item_type = (response_data['data']['featured']['entries'][x]['items'][0]['type']['value'])
                #if it's an outfit it is likely going to have an accessory
                if item_type == 'outfit':
                    #check if there are accessories with the skin by checking for length of the current entry
                    if len(response_data['data']['featured']['entries'][x]['items']) > 1:
                        if str(response_data['data']['featured']['entries'][x]['items'][1]['images']['featured']) != 'None':
                            backbling_image = str(response_data['data']['featured']['entries'][x]['items'][1]['images']['featured'])
                        elif str(response_data['data']['featured']['entries'][x]['items'][1]['images']['icon']) != 'None':
                            backbling_image = str(response_data['data']['featured']['entries'][x]['items'][1]['images']['icon'])
                        elif str(response_data['data']['featured']['entries'][x]['items'][1]['images']['smallIcon']) != 'None':
                            backbling_image = str(response_data['data']['featured']['entries'][x]['items'][1]['images']['smallIcon'])
                    else:
                        #if theres nothing then set backbling_image as nothing to 'None' to prevent possible crashing
                        backbling_image = 'None'
                section_id = (response_data['data']['featured']['entries'][x]['sectionId'])
                #set item type as a number from the dictionary made earlier to make sorting work as intended
                item_type = item_order[str(item_type)]
                #make sure price is 'finalPrice' so that bundles display correct price
                price = str(response_data['data']['featured']['entries'][x]['finalPrice'])
                item_yesterdate = (response_data['data']['featured']['entries'][x]['items'][0]['shopHistory'][len(response_data['data']['featured']['entries'][x]['items'][0]['shopHistory']) - 2])
                item_yesterdate = item_yesterdate[0:10]
                item_yesterdate = (f'{item_yesterdate[8:10]}-{item_yesterdate[5:7]}-{item_yesterdate[0:4]}')
                item_yesterdate = [item_yesterdate]
                if check_date(item_yesterdate):
                    new_items += 1
                #set current item 
                shop_current_item = [image, item, layout_id, item_type, backbling_image, section_id, price, item_yesterdate]
                #again, check if already in the array
                if shop_current_item[1] in shop_items[1]:
                    pass
                else:
                    #if not, append
                    shop_items.append(shop_current_item)
            except Exception:
                pass
    FNNewItems_path = r'C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\FNNewItems.csv'
    new_items = [new_items]
    with open(FNNewItems_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(new_items)

    import operator
    #sort in order
    #2 = layout_id = all items connected (groups starwars, marvel, etc)
    #5 = section_id = all items that are directly connected (groups items with same set name)
    #3 = item_type = dictionary made (sorts bundle - skin - etc)
    shop_items = sorted(shop_items, key=operator.itemgetter(2, 5, 3))
    #loop through list to print just for an output to make sure its working
    for i in range (0, len(shop_items)):
        print(shop_items[i][1])
    #get an image based on data
    output_shop = get_shop(shop_items)
    #return the shop image received from FNShop.get_shop()
    return (output_shop, new_items)
