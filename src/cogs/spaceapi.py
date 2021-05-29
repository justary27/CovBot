from discord.colour import Color
from discord.ext.commands.core import command
from nasapy import Nasa
from discord.ext.commands import Cog
import discord
import os
from dotenv import load_dotenv
from nasapy.api import media_search

load_dotenv()

nasa = Nasa(key=os.getenv("NASA_API_KEY"))
# print(media_search(query="Sun")['items'][1])
class space(Cog):

    def __init__(self, client):
        self.client=client

    @command(name="spod", aliases=["Spod"])
    async def pic_of_the_day(self,ctx):
        nasa_dict = nasa.picture_of_the_day()
        embed = discord.Embed(
            title=nasa_dict["title"], description=f"{ctx.author.mention}, here's the picture of today!", Color=discord.Color.dark_blue())
        embed.set_image(url=nasa_dict["hdurl"])
        embed.add_field(name="Explanation", value=nasa_dict["explanation"])
        await ctx.send(embed=embed)

    @command(name="ssearch", aliases=["Ssearch"])
    async def _media_search_(self, ctx,*args):
        print(str(args[0]))
        try:
            search=media_search(query=f'{args[0]}')['items']
            alpha_xi=search[0]
            alpha_xo=search[1]
            alpha_bi=search[2]

            embed=discord.Embed(title=alpha_xi["data"][0]["title"],description=f"{ctx.author.mention}, here's what I got!",color=Color.blue())
            embed.set_image(url=alpha_xi['links'][0]['href'])
            embed.add_field(name="Description",value=alpha_xi["data"][0]['description'])
            await ctx.send(embed=embed)

            embed=discord.Embed(title=alpha_xo["data"][0]["title"],color=Color.blue())
            embed.set_image(url=alpha_xo['links'][0]['href'])
            embed.add_field(name="Description",value=alpha_xo["data"][0]['description'])
            await ctx.send(embed=embed)

            embed=discord.Embed(title=alpha_bi["data"][0]["title"],color=Color.blue())
            embed.set_image(url=alpha_bi['links'][0]['href'])
            embed.add_field(name="Description",value=alpha_bi["data"][0]['description'])
            await ctx.send(embed=embed)
        
        except IndexError:
            await ctx.message.add_reaction("⚠")
            embed=discord.Embed(title="No result found!",description="Oops! I was unable to get any search results 😅. Try searching something else!",color=Color.dark_red())
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(space(client))

