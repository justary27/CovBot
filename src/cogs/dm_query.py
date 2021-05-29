from discord.ext.commands import Cog
from discord.ext.commands.core import command
from discord.ext import tasks
class query_response(Cog):

    def __init__(self,client):
        self.client=client
    @command(name="cloc",aliases=["Cloc"])
    async def location_based(self,ctx):
        pass

    @command(name="ctype",aliases=["Ctype"])
    async def lead_type(self,ctx):
        pass

def setup(client):
    client.add_cog(query_response(client))


