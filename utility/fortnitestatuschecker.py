import requests
from bs4 import BeautifulSoup
import json
import time

discord_webhook = "https://discord.com/api/webhooks/1302167690395258880/5d2NAV1eM0_J4zd0R7JKc0YvYUwS2qt2LGqbm8iPFyzQDYrbHzIMG4W-Xct0uIDTHS3j"
url = "https://status.epicgames.com/"
ping_everyone_on_up = True
stop_when_up = True
seconds_delay = 60
ping = "@&fortnite_status_ping"

try:
    while True:

        response = requests.get(url)

        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')

            component_container = soup.find('div', class_='component-container border-color is-group open')

            if component_container:
                components = component_container.find_all('div', class_='component-inner-container')
                operational_services = []
                non_operational_services = []
                is_down = False

                for component in components:
                    name_tag = component.find('span', class_='name')
                    status_tag = component.find('span', class_='component-status')

                    if name_tag and status_tag:
                        service_name = name_tag.text.strip()
                        service_status = status_tag.text.strip()
                        formatted_message = f"> **{service_name}:** {service_status}"

                        if "Operational" in service_status:
                            operational_services.append((service_name, formatted_message))
                        else:
                            non_operational_services.append((service_name, formatted_message))
                            if "Under Maintenance" in service_status:
                                is_down = True

                operational_services.sort(key=lambda x: len(x[0]), reverse=True)
                non_operational_services.sort(key=lambda x: len(x[0]), reverse=True)

                formatted_operational = "\n".join([msg for _, msg in operational_services])
                formatted_non_operational = "\n".join([msg for _, msg in non_operational_services])

                combined_message = f"{formatted_operational}\n> \n{formatted_non_operational}"

                print("down" if is_down else "up")

                if discord_webhook != "":
                    if ping_everyone_on_up is True:
                        if is_down:
                            premsg = f"​\n`This check is made {seconds_delay} seconds`\n"
                        else:
                            premsg = f"{ping}\n`This check is made {seconds_delay} seconds`\n"
                    else:
                        premsg = f"​\n`This check is made {seconds_delay} seconds`\n"
                        
                    
                    data = {
                        "content": premsg+combined_message
                    }
                    headers = {
                        "Content-Type": "application/json"
                    }
                    response = requests.post(discord_webhook, data=json.dumps(data), headers=headers)
                    if response.status_code == 204:
                        print("Message sent to Discord successfully")
                    else:
                        print(f"Failed to send message to Discord, status code: {response.status_code}")

                if stop_when_up == True:
                    if not is_down:
                        break
            else:
                print("Component container not found")
        else:
            print("Failed to retrieve the webpage")

        time.sleep(seconds_delay)
except KeyboardInterrupt:
    exit("\nStopped VIA KeyboardInterrupt")
except ConnectionRefusedError as e:
    exit(f"ERR: Connection Refused:\n {e}")
except requests.exceptions.ConnectionError as e:
    exit(f"ERR: Connection Refused:\n {e}")