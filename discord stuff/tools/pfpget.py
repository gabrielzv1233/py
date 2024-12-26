import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

@bot.tree.command(name="getavatar", description="Get the avatar of a user")
@app_commands.describe(user="Select a user or provide a user ID")
async def get_avatar(interaction: discord.Interaction, user: discord.User):
    try:
        if user.avatar:
            avatar_url = user.avatar.url
            await interaction.response.send_message(f"{user.mention}'s profile picture:\n{avatar_url}")
        else:
            default_avatar_url = user.default_avatar.url
            await interaction.response.send_message(
                f"{user.mention} is using a default profile picture.\n{default_avatar_url}"
            )
    except Exception as e:
        await interaction.response.send_message(f"Could not find user: {e}")

@bot.tree.command(name="userinfo", description="Get information about a user")
@app_commands.describe(user="Select a user or provide a user ID")
async def user_info(interaction: discord.Interaction, user: discord.User):
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
    avatar_note = "" if user.avatar else "(using default avatar)"
    info = (
        f"**User Information:**\n"
        f"> **Name**: `{user.name}#{user.discriminator}`\n"
        f"> **Display Name**: `{user.display_name}`\n"
        f"> **ID**: `{user.id}`\n"
        f"> **Bot**: {'Yes' if user.bot else 'No'}\n"
        f"> **System User**: {'Yes' if user.system else 'No'}\n"
        f"> **Account Created**: `{user.created_at.strftime('%Y-%m-%d %H:%M:%S')}`\n"
        f"> **Avatar**: [{avatar_url}]({avatar_url}) - {avatar_note}\n"
    )
    await interaction.response.send_message(info)

bot.run("bot token")
