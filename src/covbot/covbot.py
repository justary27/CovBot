import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()


from discord.ext.commands.core import command

client = commands.Bot(command_prefix="'")
client.remove_command("help")

def no_of_guilds():
    guilds=client.guilds
    gc=0
    for guild in guilds:
        gc+=1

    return gc

@client.event
async def on_ready():
    print(" I'm on !")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Covid-19 Guidelines in {no_of_guilds()} servers!"))

@client.command()
async def load(ctx,extension):
    client.load_extension(f'src.cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    client.reload_extension(f'src.cogs.{extension}')

for filename in os.listdir('./src/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'src.cogs.{filename[:-3]}')

client.run(os.getenv('DC_TOKEN'))
