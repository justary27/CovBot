from discord.ext import commands
import discord
from discord.ext.commands.core import command

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
        # self.color = ctx.guild.get_member(client.user.id).roles


    @commands.group(invoke_without_command=True)
    async def help(self,ctx):
        embed = discord.Embed(title="Getting Help", description="Use `'<command name>` to activate !",
                              color=ctx.author.color)
        embed.set_thumbnail(
            url="https://media0.giphy.com/media/cNYkB7qjFMKOtqeBXf/giphy.gif")

        embed.add_field(name='Covid Details',
                        value="> Gives the Covid-19 information & stats.\n> Use command `'help cd`", inline=False)
        embed.add_field(name="Covid Resources",
                        value="> You can get important Leads around your residency.\n> Use command `'help cr`",inline=False)
        embed.add_field(name="Get Relaxed",
                        value="> Get Motivational quotes,Anime and Manga suggestions \n> Space facts and abitity to talk to bot\n> Use command `'help fun`",inline=False)
        embed.add_field(name="Push/Pull google sheets",
                        value="> Add or Retrive you import data to the Google Sheet\n> right from your discord app\n> We made serching way easier ! More info `'help cr`",inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def cd(self,ctx):
        embed = discord.Embed(title="Covid Details",color=discord.Color.orange())
        embed.add_field(name="Covid Stats | 📈 ",value="> Use command `'cc <country name>`\n> `'cc` gives Covid-19 Stats of India",inline=True)
        embed.add_field(name="Covid Info | 😷",value="> Gives Covid-19 info and links to important sites\n> Use command `'ci`",inline=True)
        embed.add_field(name="Covid Vaccination | 💉",value="> Gives important vaccination details and Officials links to govt. authorized sites\n> Use command `'cvac`",inline=False)
        embed.add_field(name="Covid Medicines | 💊",value="> Basic Medicines are listed, Use command `'cmed`")

        await ctx.send(embed=embed)

    @help.command()
    async def cr(self,ctx):
        embed = discord.Embed(title="Covid Resources",description="Two types databases are there, 1.Verified (v) 2.Unverified (uv)\nVerified list will have leads verified by Verifiers\nUnverified list will contain leads added by anyone in the server.",color=discord.Color.orange())
        embed.set_thumbnail(url="https://cdn.dribbble.com/users/4120890/screenshots/15134682/good_bye_covid_19_badge_gif_dribbble_ver.gif")
        embed.add_field(name="Search | 🔍",value="> `'get <type> <search>`\n> Where type could be **Place** or **Leads**\n> You can search for Leads or Places.",inline=False)
        embed.add_field(name="Add | 📌",value="> `'add <name>/<state>/<place>/<contact>/<leads>`\n> **For eg:** 'add M.Chaterjee/West Bengal/New Town,Kolkata/m@chaterjee.in/Plasma avialable for A+ groups",inline=False)
        embed.add_field(name='Get All | 📋',value="> `'getall` gives leads of top 10 newest in verified list\n> `'getall uv` gives the same from unverififed list",inline=False)
        embed.add_field(name="Verify Leads | ☑",value="> `'verify <lead_number>` **Admin/Verifiers Only**",inline=False)
        embed.add_field(name="Add to sheet",value="> `'push <lead_number>` **Admin Only**\n> lead must be **verified**",inline=False)
        embed.add_field(name="Pull data from sheet",value="> `'pull` gets data from google sheet and add it to Database",inline=False)
        await ctx.send(embed=embed)

    @help.command()
    async def fun(self,ctx):
        embed = discord.Embed(title="Get Relaxed",color=discord.Color.orange())
        embed.add_field(name="Space Facts",value="> Get space facts and pictures\n> For more info use `'help space`")
        embed.add_field(name="Anime/Manga",value="> `'anime <name>` & `'manga <name>` to get info,rating & short explaination about Anime",inline=False)
        embed.add_field(name="WallPapers",value="> `'wall` gives random wallpaper or, `'wall <category>` gives wallpaper in specific category",inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))