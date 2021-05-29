from discord.ext.commands import Cog
from discord.ext.commands.core import command

class needs_response(Cog):

    def __init__(self,client):
        self.client=client

def setup(client):
    client.add_cog(needs_response(client))
