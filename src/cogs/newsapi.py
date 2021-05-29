from discord.colour import Color
from discord.ext.commands import Cog
import discord
from discord.ext.commands.core import command
from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

load_dotenv()

class news(Cog):
    def __init__(self,client):
        self.client=client

    @command(name='news',aliases=["News","NEWS"])
    async def _news_(self,ctx,arg1):
        newsapi = NewsApiClient(os.getenv('NEWS_API_KEY'))

        top_headlines = newsapi.get_everything(q=f'{arg1}',sources='newsweek')

        articles = top_headlines['articles']
        article1 = articles[0] 
        headline1 = article1['title'] 
        content1 = article1['content'] 
        url1=article1['url'] 

        top_headlines = newsapi.get_everything(q=f'{arg1}',sources='the-hindu')
        articles = top_headlines['articles']
        article2 = articles[0] 
        headline2 = article2['title'] 
        content2 = article2['content'] 
        url2=article2['url'] 

        top_headlines = newsapi.get_everything(q=f'{arg1}',sources='the-times-of-india')
        articles = top_headlines['articles']
        articles3 = articles[0] 
        headline3 = articles3['title'] 
        content3 = articles3['content'] 
        url3=articles3['url'] 

        embed=discord.Embed(title="Search results",description=f"{ctx.author.mention}, here's what I got!",color=ctx.author.color)
        embed.add_field(name='\u200b' ,value=f'**[{headline1}]({url1})**'+f"\n {content1[:-13]}",inline=False)
        embed.add_field(name='\u200b' ,value=f'**[{headline2}]({url2})**'+f"\n {content2[:-13]}",inline=False)
        embed.add_field(name='\u200b' ,value=f'**[{headline3}]({url3})**'+f"\n {content3[:-13]}",inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(news(client))
