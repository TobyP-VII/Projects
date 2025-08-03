def get_shop(img_list):
    import urllib.request 
    from PIL import Image, ImageFont, ImageDraw
    import math
    import datetime
    import csv

    #get date to set for the csv file
    today = datetime.datetime.now()
    today = today - datetime.timedelta(hours=1)
    today = today.strftime('%d-%m-%Y')
    date = []
    date.append(today)
    #get paths into variables so that the file has permissions
    font_path = r'C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\Fortnite.ttf'
    #set seperate font for title and items for different sizes
    title_font = ImageFont.truetype(font_path, 100)

    FNShopDate_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\FNShopDate.csv"
    with open(FNShopDate_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(date)

    #set base array for use later
    img_list_resized = []
    gfg_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\gfg.png"
    logo_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\VIIBot logo.png"
    vbuck_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\vbucks price icon.png"
    #placeholder image found on google
    urllib.request.urlretrieve('https://static.wikia.nocookie.net/fortnite/images/d/df/Glacial_Legends_Pack_-_Placeholder_-_Fortnite.png/revision/latest/thumbnail/width/360/height/360?cb=20221116193925', gfg_path)

    placeholder_img = Image.open(gfg_path) 
    placeholder_img = placeholder_img.resize((206, 206))

    gfg_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\gfg.png"
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

                    except:
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
            except:
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
                except:
                    img = placeholder_img
                    new_img.paste(img, (img_size * i, (img_size * x) + 206), img)
                img_count += 1

    #brint how many rows there are for debugging
    print(math.ceil(len(img_list_resized)/frameXamount))

    #set path for the image so that the file has permissions
    FortniteShop_path = r"C:\vs code\experiments\web scraper\fortnite stats\discord_bot_v2\FortniteShop.png"
    #save the image so the bot can output it
    new_img = new_img.convert("RGB")
    new_img.save(fp = FortniteShop_path, format = 'PNG')
