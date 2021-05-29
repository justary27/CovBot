from discord.ext.commands import Cog
from discord.ext.commands.core import command

class role_response(Cog):

    def __init__(self,client):
        self.client=client

def setup(client):
    client.add_cog(role_response(client))
