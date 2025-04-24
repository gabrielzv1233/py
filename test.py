import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
@commands.is_owner()
async def wipe(ctx):
    await ctx.send("Wiping all channels and categories...")
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            print(f"Deleted {channel.name}")
        except Exception as e:
            print(f"Could not delete {channel.name}: {e}")
    await ctx.send("Server wipe complete.")
    
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready! Logged in as {bot.user}")
    print(f"Invite link: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&integration_type=0&scope=bot")

bot.run("bot token")
