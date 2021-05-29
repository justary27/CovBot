from discord.ext.commands.core import command
import tekore as tk
import discord
from discord.ext.commands import Cog

class Spotify(Cog):

    def __init__(self,client):
        self.client=client

    @command(name="ssuggest",aliases=["Ssugest","SSugest"])
    async def song_suggest(self,ctx):
        pass

def setup(client):
    client.add_cog(Spotify(client))
