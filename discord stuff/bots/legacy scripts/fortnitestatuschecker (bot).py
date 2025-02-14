import discord
import requests
from bs4 import BeautifulSoup
import asyncio
from discord.ext import commands

BOT_TOKEN = 'Bot token here'
url = "https://status.epicgames.com/"
seconds_delay = 60
stop_when_up = True  # Recommended to be true to prevent spam
operational_notifications_only = True  # Recommended to be true to prevent spam

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

notify_users = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Fortnite's status"))

    try:
        await bot.tree.sync()
        print("Commands synced successfully.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    bot.loop.create_task(background_check_status())

async def get_current_status():
    print("Fetching current Fortnite status...")
    try:
        response = requests.get(url)
        print(f"HTTP GET {url} responded with status code {response.status_code}")

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print("Successfully parsed HTML content.")

            component_container = soup.find('div', class_='child-components-container')
            if not component_container:
                print("Failed to find child-components-container in HTML.")
                return "Failed to parse Fortnite status.", True

            component_messages = []
            components = component_container.find_all('div', class_='component-inner-container')
            print(f"Found {len(components)} components in the status page.")
            
            global services_down
            services_down = False 
            
            up_count = 0
            
            for component in components:
                name_tag = component.find('span', class_='name')
                status_attribute = component.get('data-component-status', '').strip()
                if name_tag and status_attribute:
                    service_name = name_tag.text.strip()
                    if status_attribute == 'operational':
                        service_status = 'Operational'
                    elif status_attribute == 'under_maintenance':
                        service_status = 'Under Maintenance'
                    else:
                        service_status = status_attribute.replace('_', ' ').capitalize()

                    print(f"Service detected: {service_name}, Status: {service_status}")
                    component_messages.append(f"**{service_name}:** {service_status}")
                    if service_status == "Operational":
                        up_count += 1
                else:
                    print(f"Skipped a component due to missing data: {component}")

            formatted_components = "\n".join(f"> {msg}" for msg in component_messages)

            combined_message = f"### Current Fortnite Status:\n{formatted_components}"
            
            if len(components) != up_count:
                services_down = True
            
            return combined_message, services_down

    except Exception as e:
        print(f"Error in get_current_status: {e}")

    return "Failed to retrieve status.", True


async def perform_status_check():
    print("Performing status check...")
    status_message, is_down = await get_current_status()

    global stop_when_up, services_down


    if stop_when_up:
        if not is_down and services_down:
            print("All services are operational. Stopping updates due to 'stop_when_up'.")
            services_down = False

            for user_id in notify_users:
                try:
                    user = await bot.fetch_user(user_id)
                    await user.send("All services are now operational! 🎉")
                    print(f"Notified user ID {user_id} that all services are operational.")
                except discord.Forbidden:
                    print(f"Failed to send operational notification to user ID {user_id} (Forbidden).")

            return 

    if operational_notifications_only:
        if is_down:
            print("Servers are not up, canceling message.")
            return
    
    if notify_users:
        print("Sending status update to subscribed users...")
        for user_id in notify_users:
            try:
                user = await bot.fetch_user(user_id)
                await user.send(status_message)
                print(f"Sent notification to user ID: {user_id}")
            except discord.Forbidden:
                print(f"Failed to send notification to user ID: {user_id} (Forbidden).")
        print("Status update sent to subscribed users.")
    else:
        print("No users to notify.")

    if stop_when_up:
        if not is_down:
            print("All services are operational. Unsubscribing all users due to 'stop_when_up'.")
            notify_users = []
            
async def background_check_status():
    while True:
        print("Background status check triggered.")
        if notify_users:
            await perform_status_check()
        else:
            print("No subscribed users to notify. Skipping status check.")
        await asyncio.sleep(seconds_delay)
            
@bot.tree.command(name="purge", description="Deletes the bot's own messages (DMs only)")
async def purge(interaction: discord.Interaction):
    if isinstance(interaction.channel, discord.DMChannel):
        await interaction.response.send_message("Purging the bot's messages...", ephemeral=True)
        async for message in interaction.channel.history(limit=100):
            if message.author == bot.user:
                try:
                    await message.delete()
                    await asyncio.sleep(0.5)
                except discord.Forbidden:
                    await interaction.followup.send("Cannot delete messages: Missing permissions.", ephemeral=True)
                    break
                except discord.HTTPException as e:
                    await interaction.followup.send(f"Error deleting messages: {e}", ephemeral=True)
                    break
        await interaction.followup.send("Bot message purging has been completed.", ephemeral=True)
    else:
        await interaction.response.send_message("This command can only be used in DMs.", ephemeral=True)

@bot.tree.command(name="notify", description="Checks Fortnite server status. If servers are down, you will receive a DM when they are back up or at the next check (based on configuration).")
async def notify(interaction: discord.Interaction):
    send_ephemeral = False
    if not isinstance(interaction.channel, discord.DMChannel):
        send_ephemeral = True

    user = interaction.user
    print(f"Command '/notify' executed by user ID: {user.id}")

    if user.id not in notify_users:
        current_status, is_down = await get_current_status()
        if is_down:
            notify_users.add(user.id)
            print(f"User ID: {user.id} successfully subscribed to notifications.")
        try:
            await interaction.response.send_message(f"""### You will now be notified about the status of the Fortnite servers (checks made every {seconds_delay} seconds)
                                                    > You can stop messages at any time using `/stopnotify`
                                                    > If all services are operational, you will stop getting notifications
                                                    > You can clear bot messages using `/purge`
                                                    {current_status}""", ephemeral=send_ephemeral)
        except discord.Forbidden:
            await interaction.response.send_message("Unable to send you DMs. Please ensure your DMs are open.", ephemeral=send_ephemeral)
            print(f"Failed to send confirmation DM to user ID: {user.id}")
    else:
        await interaction.response.send_message("You are already subscribed to Fortnite status notifications.", ephemeral=send_ephemeral)
        print(f"User ID: {user.id} is already subscribed.")@bot.tree.command(name="notify")
async def notify(interaction: discord.Interaction):
    send_ephemeral = False
    if not isinstance(interaction.channel, discord.DMChannel):
        send_ephemeral = True

    user = interaction.user
    print(f"Command '/notify' executed by user ID: {user.id}")

    if user.id not in notify_users:
        current_status, is_down = await get_current_status()
        if is_down:
            notify_users.add(user.id)
            print(f"User ID: {user.id} successfully subscribed to notifications.")
        try:
            await interaction.response.send_message(f"""### You will now be notified about the status of Fortnite servers (checks made every {seconds_delay} seconds)
                                                    > You can stop notifications at any time using `/stopnotify`.
                                                    > Notifications will stop automatically when all services are operational.
                                                    > Clear bot messages using `/purge`.
                                                    {current_status}""", ephemeral=send_ephemeral)
        except discord.Forbidden:
            await interaction.response.send_message("Unable to send you DMs. Please ensure your DMs are open.", ephemeral=send_ephemeral)
            print(f"Failed to send confirmation DM to user ID: {user.id}")
    else:
        await interaction.response.send_message("You are already subscribed to Fortnite status notifications.", ephemeral=send_ephemeral)
        print(f"User ID: {user.id} is already subscribed.")

@bot.tree.command(name="stopnotify")
async def stopnotify(interaction: discord.Interaction):
    send_ephemeral = False
    if not isinstance(interaction.channel, discord.DMChannel):
        send_ephemeral = True

    user = interaction.user
    print(f"Command '/stopnotify' executed by user ID: {user.id}")

    if user.id in notify_users:
        notify_users.remove(user.id)
        try:
            await interaction.response.send_message("You have unsubscribed from Fortnite status notifications. Clear bot messages using `/purge`.", ephemeral=send_ephemeral)
            print(f"User ID: {user.id} successfully unsubscribed.")
        except discord.Forbidden:
            print(f"Failed to send unsubscribe confirmation DM to user ID: {user.id}")
    else:
        await interaction.response.send_message("You are not currently subscribed to Fortnite status notifications.", ephemeral=send_ephemeral)
        print(f"User ID: {user.id} is not subscribed.")

bot.run(BOT_TOKEN)
