from discord.ext import commands
import discord
import json
import os

TOKEN = "bot token"

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready! Logged in as {bot.user}")
    print(f"Invite link: https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&integration_type=0&scope=bot")

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

@bot.tree.command(name="exportserverinfo", description="Exports all server roles, members, categories, and channels into a file.")
async def export_server_info(interaction: discord.Interaction):
    guild = interaction.guild
    if not guild:
        await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
        return

    if interaction.user != guild.owner and (not interaction.user.guild_permissions.administrator or interaction.user.top_role.position < guild.me.top_role.position):
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return

    data = {
        "guild_name": guild.name,
        "guild_id": guild.id,
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
        category_overwrites = category.overwrites.get(guild.default_role, None)
        is_category_private = category_overwrites is not None and not category_overwrites.view_channel

        category_data = {
            "name": category.name,
            "id": category.id,
            "is_private": is_category_private if is_category_private else None,
            "channels": []
        }

        for channel in category.channels:
            everyone_overwrites = channel.overwrites.get(guild.default_role, None)
            is_private = everyone_overwrites is not None and not everyone_overwrites.view_channel
            is_synced = channel.permissions_synced

            access_roles = []
            access_users = []

            if not is_synced:
                for target, perms in channel.overwrites.items():
                    if isinstance(target, discord.Role) and perms.view_channel:
                        access_roles.append(target.id)
                    elif isinstance(target, discord.Member) and perms.view_channel:
                        access_users.append(target.id)

            channel_data = {
                "name": channel.name,
                "id": channel.id,
                "type": str(channel.type),
                "topic": channel.topic if isinstance(channel, discord.TextChannel) and channel.topic else None,
                "is_private": is_private if is_private else None,
                "is_synced": is_synced if is_synced else None,
                "allowed_roles": access_roles if access_roles else None,
                "allowed_users": access_users if access_users else None,
                "permissions": {
                    str(role.id): {perm: value for perm, value in overwrites if value is not None}
                    for role, overwrites in channel.overwrites.items() if overwrites is not None
                } if not is_synced else None
            }

            channel_data = {k: v for k, v in channel_data.items() if v not in [None, [], {}]}
            category_data["channels"].append(channel_data)

        data["categories"].append(category_data)

    data["roles"] = sorted(data["roles"], key=lambda x: x["position"], reverse=True)

    filename = f"server_info_{guild.id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    await interaction.response.send_message(f"Server information for `{guild.name}` exported:", file=discord.File(filename), ephemeral=True)
    os.remove(filename)

class RestoreView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, guild: discord.Guild, data: dict):
        super().__init__(timeout=60)
        self.interaction = interaction
        self.guild = guild
        self.data = data
        self.result = None

    async def restore_server(self, overwrite: bool):
        report = {
            "missing_roles": [],
            "missing_categories": [],
            "missing_channels": [],
            "failed_role_assignments": []
        }
        role_map = {role.name: role for role in self.guild.roles}
        new_role_map = {}
        everyone_role = self.guild.default_role

        print("\n[LOG] Starting Role Restoration...")

        for role_data in self.data.get("roles", []):
            if role_data["name"] == "@everyone":
                try:
                    if "permissions" in role_data:
                        perms = discord.Permissions(role_data["permissions"])
                        await everyone_role.edit(permissions=perms)
                        print("[LOG] Restored global permissions for `@everyone`")
                    else:
                        print("[LOG] No global permissions data for @everyone")
                except discord.Forbidden:
                    report["missing_roles"].append("@everyone (global)")
                    print("[ERROR] Could not update `@everyone` global permissions")
                break  

        restored_any_roles = False
        for role_data in self.data.get("roles", []):
            if role_data["name"] == "@everyone":
                continue

            role_name = role_data["name"]
            role_color = discord.Color(int(role_data["color"].replace("#", ""), 16)) if "color" in role_data else discord.Color.default()
            role_mentionable = role_data.get("mentionable", False)
            role_hoist = role_data.get("hoist", False)

            if role_name in role_map:
                existing_role = role_map[role_name]
                new_role_map[role_data["id"]] = existing_role.id
                if overwrite:
                    try:
                        await existing_role.edit(color=role_color, mentionable=role_mentionable, hoist=role_hoist)
                        print(f"[LOG] Overwrote role: {role_name} (ID: {existing_role.id})")
                    except discord.Forbidden:
                        report["missing_roles"].append(role_name)
                        print(f"[ERROR] Missing permissions to overwrite role: {role_name}")
                else:
                    print(f"[LOG] Role exists (skipped overwrite): {role_name} (ID: {existing_role.id})")
            else:
                try:
                    new_role = await self.guild.create_role(
                        name=role_name,
                        color=role_color,
                        mentionable=role_mentionable,
                        hoist=role_hoist
                    )
                    new_role_map[role_data["id"]] = new_role.id
                    restored_any_roles = True
                    print(f"[LOG] Created role: {role_name} (New ID: {new_role.id})")
                except discord.Forbidden:
                    report["missing_roles"].append(role_name)
                    print(f"[ERROR] Could not create role: {role_name}")

        for role_data in self.data.get("roles", []):
            if role_data["name"] == "@everyone":
                continue
            old_role_id = role_data["id"]
            new_role_id = new_role_map.get(old_role_id)
            if new_role_id:
                restored_role = discord.utils.get(self.guild.roles, id=new_role_id)
                if restored_role:
                    print(f"\n[LOG] Assigning users to role: {restored_role.name} (ID: {restored_role.id})")
                    for user_id in role_data.get("members", []):
                        member = self.guild.get_member(user_id)
                        if member:
                            try:
                                await member.add_roles(restored_role)
                                print(f"[SUCCESS] Assigned {member.name} ({member.id}) to {restored_role.name}")
                            except discord.Forbidden:
                                report["failed_role_assignments"].append(f"{member.id} -> {restored_role.name}")
                                print(f"[ERROR] Could not assign {member.name} ({member.id}) to {restored_role.name}")
                        else:
                            report["failed_role_assignments"].append(f"User not found: {user_id}")
                            print(f"[ERROR] User not found: {user_id}")

        category_map = {category.name: category for category in self.guild.categories}
        for category_data in self.data.get("categories", []):
            category_name = category_data["name"]
            is_private = category_data.get("is_private", False)

            if category_name in category_map:
                category = category_map[category_name]
            else:
                try:
                    category = await self.guild.create_category(name=category_name)
                    print(f"[LOG] Created category: {category_name}")
                    if is_private:
                        await category.set_permissions(everyone_role, view_channel=False)
                        print(f"[LOG] Set category {category.name} to private")
                except discord.Forbidden:
                    report["missing_categories"].append(category_name)
                    print(f"[ERROR] Could not create category: {category_name}")
                    continue

            for channel_data in category_data.get("channels", []):
                channel = discord.utils.get(self.guild.channels, name=channel_data["name"])
                is_private = channel_data.get("is_private", False)
                is_synced = channel_data.get("is_synced", False)

                if channel:
                    if overwrite:
                        try:
                            if isinstance(channel, discord.TextChannel):
                                await channel.edit(topic=channel_data.get("topic", channel.topic))

                            if is_synced:
                                await channel.edit(sync_permissions=True)
                                print(f"[LOG] Synced channel: {channel.name} to category")
                            elif is_private:
                                await channel.set_permissions(everyone_role, view_channel=False)
                                print(f"[LOG] Set channel {channel.name} to private")
                        except discord.Forbidden:
                            report["missing_channels"].append(channel.name)
                            print(f"[ERROR] Could not edit channel: {channel.name}")
                else:
                    try:
                        if channel_data["type"] == "text":
                            new_channel = await self.guild.create_text_channel(
                                name=channel_data["name"], category=category, topic=channel_data.get("topic")
                            )
                        elif channel_data["type"] == "voice":
                            new_channel = await self.guild.create_voice_channel(
                                name=channel_data["name"], category=category
                            )

                        if is_private:
                            await new_channel.set_permissions(everyone_role, view_channel=False)
                            print(f"[LOG] Set new channel {new_channel.name} to private")

                        if is_synced:
                            await new_channel.edit(sync_permissions=True)
                            print(f"[LOG] Synced new channel {new_channel.name} to category")
                        
                        print(f"[LOG] Created channel: {new_channel.name} in {category.name}")

                    except discord.Forbidden:
                        report["missing_channels"].append(channel_data["name"])
                        print(f"[ERROR] Could not create channel: {channel_data['name']}")

        report_msg = "**⚠️ Restore Complete!**\n"
        if report["missing_roles"]:
            report_msg += f"⚠️ Could not restore roles: {', '.join(report['missing_roles'])}\n"
        if report["missing_categories"]:
            report_msg += f"⚠️ Could not create categories: {', '.join(report['missing_categories'])}\n"
        if report["missing_channels"]:
            report_msg += f"⚠️ Could not create/edit channels: {', '.join(report['missing_channels'])}\n"

        await self.interaction.followup.send(report_msg or "✅ Restore completed successfully!")

    @discord.ui.button(label="Yes (Overwrite)", style=discord.ButtonStyle.green)
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.interaction.user:
            await interaction.response.defer()
            await self.restore_server(overwrite=True)
            self.result = True
            self.stop()

    @discord.ui.button(label="No (Skip Overwrite)", style=discord.ButtonStyle.red)
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.interaction.user:
            await interaction.response.defer()
            await self.restore_server(overwrite=False)
            self.result = False
            self.stop()

@bot.tree.command(name="restoreserverinfo", description="Restores the server structure from a JSON file.")
async def restore_server_info(interaction: discord.Interaction, file: discord.Attachment):
    if not interaction.guild:
        await interaction.response.send_message("This command must be used in a server.", ephemeral=True)
        return
    
    if interaction.user != interaction.guild.owner and (not interaction.user.guild_permissions.administrator and interaction.user.top_role.position < interaction.guild.me.top_role.position):
        await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)
        return
    
    if not file.filename.endswith(".json"):
        await interaction.response.send_message("Please upload a valid JSON file.", ephemeral=True)
        return

    file_path = f"server_restore_{interaction.guild.id}.json"
    await file.save(file_path)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        await interaction.response.send_message("Invalid JSON format.", ephemeral=True)
        os.remove(file_path)
        return
    os.remove(file_path)
    
    existing_roles = {role.name for role in interaction.guild.roles}
    existing_categories = {cat.name for cat in interaction.guild.categories}
    existing_channels = {ch.name for ch in interaction.guild.channels}
    
    needs_overwrite = any(
        role["name"] in existing_roles for role in data.get("roles", [])
    ) or any(
        cat["name"] in existing_categories for cat in data.get("categories", [])
    ) or any(
        ch["name"] in existing_channels for cat in data.get("categories", []) for ch in cat.get("channels", [])
    )
    
    if needs_overwrite:
        view = RestoreView(interaction, interaction.guild, data)
        await interaction.response.send_message("Some roles, categories, or channels already exist. Overwrite them?", ephemeral=True, view=view)
    else:
        await RestoreView(interaction, interaction.guild, data).restore_server(overwrite=False)

bot.run(TOKEN)
