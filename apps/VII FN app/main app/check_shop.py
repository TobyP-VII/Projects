
import requests
import json
import csv
import datetime
import operator
import urllib.request 
from PIL import Image, ImageFont, ImageDraw
import math

def check_shop():

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
    
def get_shop(img_list):

    #get date to set for the csv file
    today = datetime.datetime.now()
    today = today - datetime.timedelta(hours=1)
    today = today.strftime('%d-%m-%Y')
    date = []
    date.append(today)
    #get paths into variables so that the file has permissions
    font_path = r'C:\vs code\apps\VII FN app\Fortnite.ttf'
    #set seperate font for title and items for different sizes
    title_font = ImageFont.truetype(font_path, 100)

    FNShopDate_path = r"C:\vs code\apps\VII FN app\FNShopDate.csv"
    with open(FNShopDate_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(date)

    #set base array for use later
    img_list_resized = []
    gfg_path = r"C:\vs code\apps\VII FN app\gfg.png"
    logo_path = r"C:\vs code\apps\VII FN app\VIIBot logo.png"
    vbuck_path = r"C:\vs code\apps\VII FN app\vbucks price icon.png"
    #placeholder image found on google
    urllib.request.urlretrieve('https://static.wikia.nocookie.net/fortnite/images/d/df/Glacial_Legends_Pack_-_Placeholder_-_Fortnite.png/revision/latest/thumbnail/width/360/height/360?cb=20221116193925', gfg_path)

    placeholder_img = Image.open(gfg_path) 
    placeholder_img = placeholder_img.resize((206, 206))

    gfg_path = r"C:\vs code\apps\VII FN app\gfg.png"
    #for all entries in array
    for i in range(0, len(img_list)):
        #check for if there is an image
        if str(img_list[i][0]) != 'None':
            #try to create an image
            try:
                urllib.request.urlretrieve(img_list[i][0], gfg_path)
            
                img = Image.open(gfg_path) 
                img = img.resize((206, 206))
                img = img.convert("RGBA")

                #if backbling image exists
                if str(img_list[i][4]) != 'None':
                    #print the skin for debugging
                    print(img_list[i][1])
                    #try except to stop possible crashes
                    try:
                        urllib.request.urlretrieve(img_list[i][4], gfg_path)

                        #get backbling image and resize it
                        backbling = Image.open(gfg_path) 
                        backbling = backbling.resize((60, 60))
                        backbling = backbling.convert("RGBA")

                        #place backbling image at the top left of the base image
                        img.paste(backbling, (0, 0), backbling)

                    except Exception:
                        pass

                #set a background that is begger than the base image for a boarder
                background = Image.new('RGBA',(210, 210), (64, 58, 213))
                background.paste(img, (0, 0), img)

                #crreate copy and make bottom part black
                dark = background.copy()
                draw  = ImageDraw.Draw(dark)
                #draw a black box over a part of the image
                draw.rectangle((0, int(0.8*206), 206, 206), 0)

                #blend darkened copy over top of background to make a faint dark box
                blended = Image.blend(background, dark, 0.2)
                #get item name
                item_name = img_list[i][1]
                #get item price
                price = img_list[i][6]
                #set item text font here so that it can be changed later on without messing up another item
                items_font = ImageFont.truetype(font_path, 20)
                draw  = ImageDraw.Draw(blended)
                #draw price at bottom left
                draw.text((25, 196), price, (255, 255, 255), anchor="lm", font = items_font)
                #check if name is bigger that 23 characters and if so, make size of font smaller to make the word fit in box
                if len(item_name) > 23:
                    font_size = 20 + ((23 - len(item_name))/2)
                    items_font = ImageFont.truetype(font_path, int(font_size))
                #draw item name text at the top of the dark box in the center
                draw.text((103, int((0.8*206) + 2)), item_name, (255, 255, 255), anchor="mt", font = items_font)

                #draw a boarder (for some reason the boarder seems to be 2 pixels off on the y value)
                draw.line((0, 0) + (0, 206), fill=(64, 58, 213), width = 4)
                draw.line((0, 206) + (206, 206), fill=(64, 58, 213), width = 4)
                draw.line((206, 206) + (206, 0), fill=(64, 58, 213), width = 4)
                draw.line((206, 2) + (0, 2), fill=(64, 58, 213), width = 4)

                #get vbuck icon to put next to price
                vbuck_icon = Image.open(vbuck_path)
                #put vbuck icon on the image
                blended.paste(vbuck_icon, (3, 184), vbuck_icon)
                #add this image to a new list
                img_list_resized.append(blended)
            except Exception:
                pass
    #after all items are done, print
    print("SHOP IMAGE COMPLETE")

    #how many icons across the x value
    frameXamount = 9
    #set width of frame
    frame_sizeX = 206 * frameXamount
    #set height of frame based on how many items are there
    frame_sizeY = ((len(img_list_resized))/frameXamount) * 206

    def roundup(x):
        return int(math.ceil(x / 206)) * 206
    #round to nearest 256 so that the icons fit correctly
    #also plus 256 for the upper boarder to show the date and logo and also a bar at the bottom
    frame_sizeY = (roundup(frame_sizeY)) + 256

    frame_size = (int(frame_sizeX), int(frame_sizeY))
    img_size = (206, 206)
    #getting the image size of the items
    img_size = 206
    #create a new image with the frame size 
    new_img = Image.new('RGBA',(frame_size), (103, 97, 242))
    logo_img = Image.open(logo_path)
    logo_img = logo_img.convert("RGBA")
    #paste the logo at the top left of the new image
    new_img.paste(logo_img, (0, 0), logo_img)
    draw = ImageDraw.Draw(new_img)
    #draw text of the current date and the title and paste them at the top of the screen
    draw.text(((new_img.width)/2, 100), str(date)[1:-1], (255, 255, 255), anchor="ms", font = title_font)
    draw.text(((new_img.width)/2, 101), 'ITEM SHOP', (255, 255, 255), anchor="mt", font = title_font)

    #get the count to go though each image
    img_count = 0
    #for x in (however many icons are up the y value aka; 0 -> 8 icons = 1 row, 9 -> 17 icons = 2 rows etc)
    for x in range(math.ceil(len(img_list_resized)/frameXamount)):
        #for i in (how many images in the x value)
        for i in range(frameXamount):
            #check if the image count is over the size of the list so that the final image doesnt get pasted multiple times to fill the screen and/or crash
            if img_count < len(img_list_resized):
                #try placing the image
                try:
                    img = img_list_resized[img_count]
                    new_img.paste(img, (img_size * i, (img_size * x) + 206), img)
                #if cant place image then it doesnt exist and therefore should place placeholder image
                except Exception:
                    img = placeholder_img
                    new_img.paste(img, (img_size * i, (img_size * x) + 206), img)
                img_count += 1

    #brint how many rows there are for debugging
    print(math.ceil(len(img_list_resized)/frameXamount))

    #set path for the image so that the file has permissions
    FortniteShop_path = r"C:\vs code\apps\VII FN app\FortniteShop.png"
    #save the image so the bot can output it
    new_img = new_img.convert("RGB")
    new_img.save(fp = FortniteShop_path, format = 'PNG')