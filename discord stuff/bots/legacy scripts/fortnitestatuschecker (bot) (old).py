import discord
import requests
from bs4 import BeautifulSoup
import asyncio
from discord.ext import commands

BOT_TOKEN = 'bot token here'
url = "https://status.epicgames.com/"
ping_role_id = 1302167334491918357
seconds_delay = 1
stop_when_up = True

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_two_messages = []
status_check_running = False
default_channel_id = None
active_channel = None

def has_admin_permissions(interaction):
    return interaction.user.guild_permissions.administrator

async def update_bot_status(is_down):
    if is_down:
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="Fortnite's status"))
    else:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="Fortnite's status"))

async def perform_status_check():
    global last_two_messages, status_check_running, stop_when_up, active_channel
    print("Active channel " + str(active_channel))
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        component_container = soup.find('div', class_='component-container border-color is-group')

        
        if component_container:
            components = component_container.find_all('div', class_='component-inner-container')
            is_down = False
            
            operational_services = []
            non_operational_services = []
            
            for component in components:
                name_tag = component.find('span', class_='name')
                status_tag = component.find('span', class_='component-status')
                if name_tag and status_tag:
                    service_name = name_tag.text.strip()
                    service_status = status_tag.text.strip()
                    
                    formatted_message = f"> **{service_name}:** {service_status}"
                    if "Operational" in service_status:
                        operational_services.append(formatted_message)
                    else:
                        non_operational_services.append(formatted_message)
                        is_down = True
            print(f"checked ({is_down})")
            formatted_operational = "\n".join(operational_services)
            formatted_non_operational = "\n".join(non_operational_services)
            
            if formatted_non_operational.strip():
                combined_message = f"{formatted_operational}\n> \n{formatted_non_operational}"
            else:
                combined_message = f"{formatted_operational}"
            
            await update_bot_status(is_down)
            
            if status_check_running and active_channel:
                premsg = f"<@&{ping_role_id}>\n" if not is_down else f"​\n`Updated every {seconds_delay} seconds`"
                new_message = await active_channel.send(premsg + combined_message)

                last_two_messages.append(new_message)
                if len(last_two_messages) > 2:
                    old_message = last_two_messages.pop(0)
                    try:
                        await old_message.delete()
                    except discord.HTTPException as e:
                        print(f"Failed to delete oldest message: {e}")
                
                if stop_when_up and not is_down:
                    status_check_running = False
                    await active_channel.send("All services are up. Stopping checks.")
                    print("Stopped (services up)")

async def background_check_status():
    while True:
        if status_check_running:
            await perform_status_check()
        await asyncio.sleep(seconds_delay)

@bot.event
async def on_ready():
    global active_channel
    print(f'Logged in as {bot.user}')

    if default_channel_id:
        active_channel = bot.get_channel(default_channel_id)
        if active_channel:
            print(f"Active channel set to default channel: {active_channel.name}")

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Fortnite's status"))

    try:
        await bot.tree.sync()
        print("Commands synced.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    bot.loop.create_task(background_check_status())

@bot.tree.command(name="start", description="Start checking the Fortnite service status.")
async def start(interaction: discord.Interaction):
    if not has_admin_permissions(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    global status_check_running, active_channel
    if not active_channel:
        active_channel = interaction.channel

    if status_check_running:
        await interaction.response.send_message("Status check is already running.", ephemeral=True)
    else:
        status_check_running = True
        await interaction.response.send_message("Started status check.")
    print("Started")

@bot.tree.command(name="stop", description="Stop checking the Fortnite service status.")
async def stop(interaction: discord.Interaction):
    if not has_admin_permissions(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    global status_check_running
    if status_check_running:
        status_check_running = False
        await interaction.response.send_message("Stopped status check.")
    else:
        await interaction.response.send_message("Status check is not currently running.", ephemeral=True)
    print("Stopped")

@bot.tree.command(name="stop_when_up", description="Toggle stopping checks when all services are up.")
async def stop_when_up_cmd(interaction: discord.Interaction):
    if not has_admin_permissions(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    global stop_when_up
    stop_when_up = not stop_when_up
    status = "enabled" if stop_when_up else "disabled"
    await interaction.response.send_message(f"`stop_when_up` is now {status}.", ephemeral=True)

@bot.tree.command(name="set_active_channel", description="Set the active channel for status updates.")
async def set_active_channel(interaction: discord.Interaction):
    if not has_admin_permissions(interaction):
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    global active_channel
    active_channel = interaction.channel
    await interaction.response.send_message(f"Active channel for updates set to: {active_channel.mention}", ephemeral=True)

bot.run(BOT_TOKEN)
