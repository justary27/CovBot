from discord.ext.commands import Cog
from discord.ext.commands.core import command

class Leads(Cog):
    def __init__(self,client):
        self.client=client

    @command(name="clead",aliases=["addlead","leadadd"])
    async def Add_lead(self,ctx,*args):
        pass

    @command(name="dlead",aliases=["displaylead","leaddisplay"])
    async def display_lead(self,ctx,*args):
        pass

    @command(name="rlead",aliases=["removelead","leadremove"])
    async def remove_lead(self,ctx,*args):
        pass

def setup(client):
    client.add_cog(Leads(client))
