import httpx
from selectolax.parser import HTMLParser
from twilio.rest import Client

results = []

def end_program():
    while True:
        end = input("Are you sure you want to end?: ")
        if end == "yes":
            quit()
        elif end == "no":
            break
        else:
            pass

while True:
    account_name = input("Enter an account name: ")
    if account_name == "end":
        break
    else:
        account_url_name = account_name.replace(" ", "%20")
        account_url = "https://fortnitetracker.gg/profile/v2/" + account_url_name

        def get_data(account, url, selector):
            resp = httpx.get(
                url
                )
            html = HTMLParser(resp.text)
            wins = html.css_first(selector).text().strip()
            return {"account": account, "wins": wins}
        try:
            def main():
                results.append(
                    get_data(
                        account_name,
                        account_url,
                        "div.f-4-size-and-color"
                    )
                )
                print(results)
            if __name__ == "__main__":
                main()
        except:
            print("No account with that name found... ")


while True:
    send_message = input("send message?: ")
    if send_message.lower() == "yes":
        account_sid = ''
        auth_token = ''
        client = Client(account_sid, auth_token)

        while True:
            while True:
                send_to = input("who: ")
                if send_to == "me":
                    send_to = "+447706716104"
                    break
                elif send_to == "chris":
                    send_to = "+447395778779"
                    break
                elif send_to == "cole":
                    send_to = "+447305675262"
                    break
                else:
                    break
            if send_to == "noone":
                end_program()
            else:
                try:
                    message = client.messages.create(
                        messaging_service_sid='MG0418f132deb01bc15b81751c221deb34',
                        body=str(
                            results
                        ).replace("{", "\n").replace("},", "").replace("}", "").replace("'", ""),
                        to=send_to
                    )
                    break
                except:
                    print("No number found... ")
    
    elif send_message.lower() == "no":
        end_program()
    else:
        pass