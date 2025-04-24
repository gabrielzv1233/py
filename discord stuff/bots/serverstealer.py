# to use with restore bot
# all this does is exports the server info as soon as its invited, and leaves
from discord.ext import commands
import requests
import discord
import json
import os

TOKEN = "bot token"
WEBHOOK_URL = "webhook" # Set this to your webhook URL, or leave empty to disable uploading
DELETE_AFTER_UPLOAD = True # Only works if WEBHOOK_URL is set

intents = discord.Intents.default()
intents.guilds = True # Required to detect when the bot joins a server
intents.members = True # Needed to export members in role

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    print(f"Invite link: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=268436496&integration_type=0&scope=bot")

@bot.event
async def on_guild_join(guild: discord.Guild):
    print(f"[LOG] Joined server: {guild.name} (ID: {guild.id})")
    
    data = {
        "guild_name": guild.name,
        "guild_id": guild.id,
        "icon_url": guild.icon.url if guild.icon else None,
        "splash_url": guild.splash.url if guild.splash else None,
        "banner_url": guild.banner.url if guild.banner else None,
        "description": guild.description if guild.description else None,
        "roles": [],
        "categories": []
    }

    for role in guild.roles:
        role_data = {
            "name": role.name,
            "id": role.id,
            "color": str(role.color) if role.color.value != 0 else None,
            "permissions": role.permissions.value if role.permissions.value != 0 else None,
            "members": [member.id for member in role.members] if role.members else None,
            "position": role.position,
            "hoist": role.hoist if role.hoist else None,
            "mentionable": role.mentionable if role.mentionable else None
        }
        role_data = {k: v for k, v in role_data.items() if v not in [None, [], {}]}
        data["roles"].append(role_data)

    for category in guild.categories:
        category_data = {
            "name": category.name,
            "id": category.id,
            "channels": []
        }
        for channel in category.channels:
            channel_data = {
                "name": channel.name,
                "id": channel.id,
                "type": str(channel.type),
                "topic": channel.topic if isinstance(channel, discord.TextChannel) and channel.topic else None,
                "is_private": len(channel.overwrites) > 0,
                "permissions": {
                    str(target.id): {perm: value for perm, value in overwrites if value is not None}
                    for target, overwrites in channel.overwrites.items() if overwrites is not None
                }
            }
            channel_data = {k: v for k, v in channel_data.items() if v not in [None, [], {}]}
            category_data["channels"].append(channel_data)
        data["categories"].append(category_data)

    data["roles"] = sorted(data["roles"], key=lambda x: x["position"], reverse=True)

    filename = f"server_info_{guild.id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"[LOG] Server information saved to {filename}")

    if WEBHOOK_URL and WEBHOOK_URL.strip():
        try:
            with open(filename, "rb") as file:
                response = requests.post(WEBHOOK_URL, files={"file": file})
            
            if response.status_code == 200:
                print(f"[LOG] File uploaded successfully to webhook")
                
                if DELETE_AFTER_UPLOAD:
                    os.remove(filename)
                    print(f"[LOG] File {filename} deleted from server")
            else:
                print(f"[ERROR] Failed to upload file to webhook: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[ERROR] Exception occurred while uploading file: {e}")

    await guild.leave()
    print(f"[LOG] Left server: {guild.name} (ID: {guild.id})")

bot.run(TOKEN)
