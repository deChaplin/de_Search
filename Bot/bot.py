import asyncio
import discord
from discord import app_commands, Embed
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
import random
import guild_database
from googleapiclient.discovery import build
import requests

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

load_dotenv()
TOKEN = os.getenv('TOKEN')
GOOGLE_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
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
    #sync_commands()

    try:
        synced = await client.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print(e)

    print('Bot is ready!')
    change_status.start()
    guild_database.create_database()


async def sync_commands():
    try:
        synced = await client.tree.sync()
        print(f"Synced {synced} commands")
    except Exception as e:
        print(e)


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
    embed = create_embed("de_Search help", "Commands for the search Bot", get_random_colour(), [
        ("generate <prompt>", "Generates an image using AI", True), # TODO
        ("image <prompt>", "Gets an image", True), # TODO
        ("search <prompt>", "Searches using <> search engine", True), # TODO

        ("wiki <prompt>", "Searches using the Wikipedia search engine", True), # TODO
        ("define <prompt>", "Searches using the Dictionary search engine", True), # TODO

        ("rezi <prompt>", "Searches using the Rezi.one search engine", True), # TODO
        ("checkPrefix", "Shows current prefix for the server", True),
        ("help", "Shows this help menu", True),
    ])

    await ctx.send(embed=embed)

# ======================================================================================================================
# Search commands
# ======================================================================================================================


@client.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello! {interaction.user.mention}")


@client.tree.command(name="image", description="Gets an image")
@app_commands.describe(arg = "image to search for")
async def image(interaction: discord.Interaction, arg: str):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=GOOGLE_KEY).cse()
    result = resource.list(q=f"{arg}", cx=SEARCH_ENGINE_ID, searchType="image").execute()
    url = result['items'][ran]['link']

    emb = create_image_embed(f"Your image - {arg}", "", get_random_colour(), url)

    await interaction.response.send_message(embed=emb, ephemeral=False)


@client.tree.command(name="search", description="Search the internet")
@app_commands.describe(arg = "search term")
async def search(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"You said {arg}")

# ======================================================================================================================
# Loop Events
# ======================================================================================================================


@tasks.loop(seconds=1)
async def change_status():
    status = [" 1", " 2", " 3 👀", " 4",
               str(get_guilds()) + " servers!"]

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name=(random.choice(status))))
    await asyncio.sleep(3)


# ======================================================================================================================
# Random functions
# ======================================================================================================================

# Function to randomly select a colour for the embed
def get_random_colour():
    return random.choice(color_codes)


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

def create_image_embed(title, description, colour, url):
    embed = discord.Embed(
        title=title,
        description=description,
        color=colour
    )

    embed.set_image(url=url)

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
