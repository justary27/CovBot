import discord
from discord.ext.commands import Cog
from discord.ext.commands.core import command
from wit import Wit

responses = ['Hello {}, How may I help?','Good morning {}, May I help you ?']
initiaters=["hi","hello","howdy","how are ya","how are you"]
class Task(Cog):
    def __init__(self, client):
        self.client = client


    @Cog.listener()
    async def on_message(self,msg):
        for x in initiaters:
            if x in str(msg.content):
                pass

    @command(aliases=['hi', 'hii', 'hello'],help='General Interaction')
    async def _hey(self, ctx):
        resp = str(f'Hello ! {ctx.author.mention} How may I help you ? ')
        await ctx.reply(resp)
        await ctx.message.add_reaction("🙋‍♀️")

        #invite the bot
    @command(name="invite",aliases=["Invite","ics"])
    async def invite_bot(self,ctx):
        invite_url=discord.utils.oauth_url(client_id="835222640821796924")
        embed=discord.Embed(title="Invite link",description="",color=discord.Color.from_rgb(198, 197, 255))
        embed.add_field(name="Here's my invite link, would love to join your server 😁!",value=f"[**Click here to invite**]({invite_url})")
        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/835222640821796924/d764c030044ca580aa43f346eda64f9e.png?size=128")
        await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(Task(client))
