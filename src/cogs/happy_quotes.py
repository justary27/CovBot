from discord.colour import Color
from discord.ext.commands import Cog
import discord
from discord.ext.commands.core import command
from requests import get
import json

class good_quotes(Cog):

    def __init__(self, client):
        self.client=client

    @command(name="gq", aliases=["GQ", "Gq"])
    async def get_good_q(self, ctx):
        data = get(url="https://zenquotes.io/api/random")
        q = json.loads(data.text)[0]["q"]
        a = json.loads(data.text)[0]["a"]
        embed = discord.Embed(
            title="Inspire yeself!", description=f"{ctx.author.mention}, time for some inspiration!", color=Color.dark_teal())
        embed.add_field(name=f"Quote by {a}",value=f"{q}",inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(good_quotes(client))

