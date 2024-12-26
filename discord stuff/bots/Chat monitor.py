from win11toast import toast_async
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await toast_async('Chat monitor is online', f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await toast_async(f'{message.guild.name} → {message.channel.name}', message.content)

client.run('Ur token')
