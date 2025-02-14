from flask import Flask, jsonify
from discord.ext import commands
from collections import deque
import threading
import markdown
import discord
import html
import re

# todo for pings, roles, @everyone and @here 

token = "token go here homie"

app = Flask(__name__)
message_cache = deque(maxlen=500)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@app.route("/")
def home():
    content = r"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="icon" href="http://discord.com/assets/favicon.ico">
            <title>Discord Message Feed</title>
                <style>
                    a:visited {
                        color: #059CE5;
                    }

                    a {
                        color: #059CE5;
                        text-decoration: none;
                    }

                    b {
                        color: F2F3F5;
                    }

                    @font-face {
                        font-family: 'Source Sans Pro';
                        src: url('https://fonts.gstatic.com/s/sourcesanspro/v14/6xK3dSBYKcSV-LCoeQqfX1RYOo3qNa7luj5Z.woff2') format('woff2');
                        font-weight: normal;
                        font-style: normal;
                    }

                    body {
                        font-family: 'Source Sans Pro', sans-serif;
                        background-color: #313338;
                        color: #DBDEE1;
                    }

                    code {
                        background-color: #2B2D31;
                        color: #DBDEE1;
                        border: 1px solid #1B1D20;
                        padding: 6px;
                        display: inline-block;
                        white-space: pre;
                        border-radius: 4px;
                        margin: 0;
                    }

                    .ping, .channel {
                        background-color: #494B6F;
                        color: #C9CDFB;
                        border-radius: 2px;
                        padding-bottom: 2px;
                        padding-left: 2px;
                        padding-right: 2px;
                        font-weight: 500;
                    }

                    .ping:hover, .channel:hover {
                        background-color: #5865F2;
                        color: #FFFFFF;
                    }

                    pre {
                        background-color: #2E3034;
                        color: #DBDEE1;
                        border: 1px solid black;
                        padding: 8px; /* Add padding for better spacing */
                        display: inline-block; /* Adjust width to content */
                        white-space: pre; /* Preserve spaces and line breaks */
                        border-radius: 4px; /* Rounded corners for better appearance */
                        margin: 8px 0; /* Add vertical spacing */
                    }
                </style>
        </head>
        <body>
            <div id="messages"></div>

            <script>
                const messagesDiv = document.getElementById("messages");
                let lastMessageCount = 0;

                async function fetchMessages() {
                    try {
                        const response = await fetch("/messages");
                        if (response.ok) {
                            const messages = await response.json();
                            if (messages.length !== lastMessageCount) {
                                lastMessageCount = messages.length;
                                updateMessages(messages);
                            }
                        } else {
                            console.error("Failed to fetch messages");
                        }
                    } catch (error) {
                        console.error("Error fetching messages:", error);
                    }
                }

                function updateMessages(messages) {
                    messagesDiv.innerHTML = "";

                    messages.forEach(msg => {
                        const messageHtml = `
                            <div class="message">
                                ${msg.channel} - ${msg.display_name}&nbsp;
                                ${msg.content}
                            </div><br>`;
                        messagesDiv.innerHTML += messageHtml;
                    });

                    messagesDiv.scrollTop = messagesDiv.scrollHeight;
                }

                setInterval(fetchMessages, 1000);
            </script>

        </body>
        </html>
        """
    return content

@app.route("/messages")
def get_messages():
    response = jsonify(list(message_cache))
    response.mimetype = "application/json"
    return response

def get_channel_name(channel_id):
    channel = bot.get_channel(int(channel_id))
    return channel.name if channel else f"unknown-channel-{channel_id}"

async def get_user_mention(user_id, guild=None):
    user = bot.get_user(int(user_id))
    if not user:
        try:
            user = await bot.fetch_user(int(user_id))
        except discord.NotFound:
            return f'<span class="ping" title="unknown-user: {user_id}">@unknown-user</span>'
    
    display_name = user.display_name
    if guild:
        member = guild.get_member(user.id)
        if member and member.nick:
            display_name = member.nick

    sysname = user.name + "#" + user.discriminator 
    return f'<span class="ping" title="{sysname}: {user_id}">@{display_name}</span>'

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    raw_content = html.escape(message.content)

    raw_content = re.sub(
        r'&lt;#(\d+)&gt;',
        lambda match: f'<span class="channel" title="{match.group(1)}"># {get_channel_name(match.group(1))}</span>',
        raw_content
    )

    async def replace_user_mention(match):
        user_id = match.group(1)
        return await get_user_mention(user_id, message.guild)

    user_mentions = re.finditer(r'&lt;@!?(\d+)&gt;', raw_content)
    for mention in user_mentions:
        raw_content = raw_content.replace(mention.group(0), await replace_user_mention(mention))

    styled_content = markdown.markdown(raw_content, extensions=['sane_lists', 'fenced_code'])
    styled_content = styled_content.replace("<p>", "").replace("</p>", "").replace("\n", "<br>")

    styled_content = re.sub(r'<br>(\s*</(pre|code|div)>)', r'\1', styled_content)
    styled_content = re.sub(r'(<(pre|code|div)[^>]*>)<br>', r'\1', styled_content)
    
    styled_content = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', styled_content)
    styled_content = re.sub(r'(http?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', styled_content)


    new_message = {
        "display_name": f'<b title="{message.author.name + "#" + message.author.discriminator}: {message.author.id}">{message.author.nick or message.author.display_name}</b>',
        "username": message.author.name,
        "content": styled_content.strip(),
        "channel": f'<span title="{message.channel.id}">#{message.channel.name}</span>'
    }

    message_cache.append(new_message)

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)

def run_discord():
    bot.run(token)

if __name__ == "__main__":
    import threading
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    run_discord()