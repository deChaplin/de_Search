import asyncio
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle
from dotenv import load_dotenv
import random
from Checker import vacChecker
import guild_database

# Setting up the client and intents
intents = discord.Intents.all()
# Setting up the bots prefix
DEFAULT_PREFIX = '!'

async def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)
    else:
        if guild_database.check_guild(message.guild.id):
            prefix = guild_database.get_prefix(message.guild.id)
            return commands.when_mentioned_or(prefix)(client, message)
        else:
            guild_database.add_guild(message.guild.id, DEFAULT_PREFIX)
            return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)

client = commands.Bot(command_prefix=get_prefix, intents=intents)
# Setting up the status to cycle through
status = cycle(["your steam accounts!", "to see who gets banned!"])

load_dotenv()
TOKEN = os.getenv('TOKEN')
KEY = os.getenv('KEY')
# Remove the default help command
client.remove_command('help')

color_codes = [
    0xFF0000,  # Red
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0xFFFF00,  # Yellow
    0xFF00FF,  # Magenta
    0x00FFFF,  # Cyan
    0xFFA500,  # Orange
    0x800080,  # Purple
    0x008000,  # Dark Green
    0x000080,  # Navy Blue
    0x800000,  # Maroon
    0x008080,  # Teal
    0xFFC0CB,  # Pink
    0xFFD700,  # Gold
    0xA52A2A,  # Brown
    0x800000,  # Dark Red
    0x00FF7F,  # Spring Green
    0x808000,  # Olive
    0x008080,  # Teal
    0x008000,  # Green
    0x000080,  # Navy
    0x0000FF,  # Blue
    0xFF00FF,  # Magenta
    0xFF0000,  # Red
    0xFFA500   # Orange
]


# ======================================================================================================================
# Standard Events
# ======================================================================================================================


@client.event
async def on_ready():
    vacChecker.start_up()
    print('Bot is ready!')
    change_status.start()
    check_vac.start()

    guild_database.create_database()


# On guild join
@client.event
async def on_guild_join(guild):
    guild_database.add_guild(guild.id, '!')
    print(f"Joined {guild.name}")


# On guild remove
@client.event
async def on_guild_remove(guild):
    guild_database.remove_guild(guild.id)
    print(f"Removed {guild.name}")


# On message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not guild_database.check_guild(message.guild.id):
        guild_database.add_guild(message.guild.id, DEFAULT_PREFIX)

    mention = f'<@{client.user.id}>'
    if message.content == mention:
        await message.channel.send("My prefix is " + guild_database.get_prefix(message.guild.id))

    if message.content.startswith(guild_database.get_prefix(message.guild.id)):
        await client.process_commands(message)


# ======================================================================================================================
# Standard Commands
# ======================================================================================================================


# Command to change the bots prefix
@client.command()
async def setPrefix(ctx, prefix):
    client.command_prefix = prefix
    guild_database.update_prefix(ctx.guild.id, prefix)
    await ctx.send(f"Prefix changed to {prefix}")


# Command to check the current prefix
@client.command()
async def checkPrefix(ctx):
    prefix = guild_database.get_prefix(ctx.guild.id)
    await ctx.send(f"Current prefix is {prefix}")


# Help command
@client.command()
async def help(ctx):
    embed = create_embed("VAC Checker Help", "Commands for the VAC Checker Bot", get_random_colour(), [
        ("status <steamID>", "Check the status of a specific account", True),
        ("add <steamID>", "Add a steam account to the database", True),
        ("remove <steamID>", "Remove a steam account from the database", True),

        ("setPrefix", "Change the prefix for the server", True),
        ("checkPrefix", "Shows current prefix for the server", True),
        ("help", "Shows this help menu", True),
    ])

    await ctx.send(embed=embed)

# ======================================================================================================================
# VAC Checker Commands
# ======================================================================================================================


# Command to check the status of a steam account
@client.command()
async def status(ctx, steam_id):
    try:
        steamID, name, game_banned, game_bans, vac_banned, vac_bans, last_ban = \
            vacChecker.check_vac(KEY, steam_id, ctx.message.author.id)

        if game_banned == "Yes" or vac_banned == "Yes":
            color = 0xFF0000
        else:
            color = 0x44ff00

        embed = create_embed("Profile Status", "The current status of " + name, color, [
            ("Name - ", name, False),
            ("Steam ID - ", steamID, False),
            ("Game Banned - ", game_banned, False),
            ("Game Bans - ", game_bans, False),
            ("VAC Banned - ", vac_banned, False),
            ("VAC Bans - ", vac_bans, False),
            ("Last Ban - ", get_days_since_ban(last_ban), False)
        ])

        await ctx.send(embed=embed)
    except:
        await ctx.send("Error checking account!")


# Command to add a steam account to the database
@client.command()
async def add(ctx, steam_id):
    try:
        name = vacChecker.add_account(KEY, steam_id, ctx.message.author.id)
        await ctx.send(f"{name} added to database!")
    except:
        await ctx.send("Error adding account to database!")


# Command to remove a steam account from the database
@client.command()
async def remove(ctx, steam_id):
    if vacChecker.remove_account(steam_id, ctx.message.author.id):
        await ctx.send("Account removed from database!")
    else:
        await ctx.send("Only the person who added the account can remove it!")

# ======================================================================================================================
# Loop Events
# ======================================================================================================================


@tasks.loop(seconds=1)
async def change_status():
    status = ["your steam accounts!", " who gets banned!", " you 👀", " people get banned",
               str(get_guilds()) + " servers!"]

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=(random.choice(status))))
    await asyncio.sleep(3)


# Loop to check for vac bans on all accounts every hour
@tasks.loop(minutes=60)
async def check_vac():

    # Get list of user ids from database
    # iterate through list to check all accounts belonging to user
    # send private message to user

    # Will run for the number of unique discord ids in the database
    discord_ids = vacChecker.get_discord_id()

    if discord_ids:
        for index, id in enumerate(discord_ids):
            user = client.get_user(int(id))

            steam_ids = vacChecker.get_steam_id(int(id))

            for s_index, s_id in enumerate(steam_ids):
                steamID, name, game_banned, game_bans, vac_banned, vac_bans, last_ban = \
                    vacChecker.check_vac(KEY, s_id, int(id))

                if game_banned == "Yes" or vac_banned == "Yes":
                    embed = create_embed("Profile Status", "The current status of " + name,
                                         get_random_colour(), [
                                             ("Name - ", name, False),
                                             ("Steam ID - ", steamID, False),
                                             ("Game Banned - ", game_banned, False),
                                             ("Game Bans - ", game_bans, False),
                                             ("VAC Banned - ", vac_banned, False),
                                             ("VAC Bans - ", vac_bans, False),
                                             ("Last Ban - ", get_days_since_ban(last_ban), False)
                                         ])
                    await user.send(embed=embed)
                    vacChecker.remove_account(steamID, int(id))
    else:
        print(f"User with ID {str(id)} not found.")


# ======================================================================================================================
# Random functions
# ======================================================================================================================

# Function to randomly select a colour for the embed
def get_random_colour():
    return random.choice(color_codes)


# Take the days since last ban and return how many days ago it was
def get_days_since_ban(days):
    if days == 0:
        return "Today"
    elif days == 1:
        return "Yesterday"
    else:
        return str(days) + " days ago"


def create_embed(title, description, colour, fields):
    embed = discord.Embed(
        title=title,
        description=description,
        color=colour
    )
    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=field[2])

    embed.set_footer(text="Developed by de_Chaplin", icon_url="https://avatars.githubusercontent.com/u/85872356?v=4")
    return embed


def get_guilds():
    try:
        guilds = guild_database.get_num_guilds()
        if guilds >= 1:
            return guilds
        else:
            return "0"
    except:
        print ("Error getting guilds")
        return "0"


client.run(TOKEN)
