import typing
import discord
import os
from discord.colour import Color
from discord.ext import commands
# import covid
# from covid import Covid
import requests
from requests.api import get
import pycountry
import datetime
from datetime import date
import json
import newsapi
from newsapi import NewsApiClient
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt
import io


load_dotenv()

# covid = Covid()
list_cont = []

class News(commands.Cog):
    def __init__(self,client):
        self.client = client

    def country_list(self):
        country = [(list(pycountry.countries)[i].name, list(pycountry.countries)[i].alpha_2) for i in range(len(pycountry.countries))]
        return country

    def conv(self,num):
        num = str(num)

        x = num[:-3]
        y = num[-3:]
        z = f',{y}'
        for i in range(int(len(x)/2)):
            t = x
            # print(t)
            x = t[:-2]
            y = t[-2:]
            # print(y)
            z = f',{y}{z}'
        if (len(num)) % 2 != 0:
            z = z[1:]
        else:
            z = f'{num[:1]}{z}'

        return z

    def active_cases(self,country):
        # list_cases = covid.get_status_by_country_name(country)
        # print(list_cases)
        d1 = datetime.datetime.now()
        date = d1.strftime("%Y-%m-%d")

        url = "https://covid-193.p.rapidapi.com/history"

        querystring = {"country": country, "day": date}

        headers = {
        'x-rapidapi-key': os.getenv("COVID_BOT_API_KEY"),
            'x-rapidapi-host': "covid-193.p.rapidapi.com"
        }

        response = requests.request(
        "GET", url, headers=headers, params=querystring)

        # print(response.text)
        dataset = (response.text)
        dataset = json.loads(dataset)
        # print((dataset))
        content = dataset['response']
        n = len(content)
        if n==1:
            m = 1
        else:
            m = n-1
        list_cases = content[len(content)-1]['cases']
        container = []
        container.append(list_cases['total'])
        container.append(list_cases['active'])
        container.append(list_cases['new'])

        list_deaths = content[len(content)-1]['deaths']
        container.append(list_deaths['total'])
        container.append(list_deaths['new'])
        container.append(content[m]['tests']['total'])
        return container

    @commands.command(aliases=['cinfo','covidinfo'],help='Gives You Covid-19 informations')
    async def _info(self,ctx):
        embed = discord.Embed(
            title='Covid-19', description='Coronavirus disease 2019 (COVID-19), also known as the coronavirus or COVID, is a contagious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). The first known case was identified in Wuhan, China, in December 2019. The disease has since spread worldwide, leading to an ongoing pandemic.\n for **more info [click here](https://en.wikipedia.org/wiki/COVID-19)**', color=discord.Color.blurple())
        embed.set_thumbnail(
            url="https://innovativegenomics.org/wp-content/uploads/2020/04/Abstract-SARS-CoV-2-in-red-with-RNA.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['cmed'])
    async def _medicine(self,ctx):
        medurl = "https://www.healthline.com/health/coronavirus-treatment"
        embed = discord.Embed(
            title='General Medicines', description=f'Although you are suggested to get advice from a Doctor\nOne can take these medicines by themselves otherwise !!\n [**know more about medicines**]({medurl})', color=discord.Color.green())

        embed.set_thumbnail(
            url='https://image.flaticon.com/icons/png/512/1098/1098028.png')
        embed.add_field(name="Acidity",value='Pentaprazole 40mg',inline=False)
        embed.add_field(name="Body Pain and Fever",value='Dolo 650mg (for body temp. > 100°F)', inline=False)
        embed.add_field(name="Cough",value='Ambroxyl or Azithromycin 500mg',inline=False)
        embed.add_field(name="Vomitting",value='Ondem 4mg',inline=False)
        embed.add_field(name="Immunity",value='B-C-D vitamins',inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['cases','ccases','cc'],help='tells covid cases in your perticular country')
    async def _cases(self,ctx,*,country='India'):
        arr = self.active_cases(country)
        # cname = pycountry.countries.get(name=country)
        # short = (cname.alpha_2).lower()
        country = country.capitalize()
        url = f'https://covid19.who.int/'
        embed = discord.Embed(
            title=f'Current Covid-19 cases in {country}',url=url,description=f"Here's the covid stats of **{country}** !",color=discord.Color.blurple())

        embed.add_field(name='Confirmed Cases',value=f'{self.conv(arr[0])}',inline=False)
        embed.add_field(name='Active Cases',value=f'{self.conv(arr[1])}',inline=True)
        embed.add_field(name='New Cases',value=f'{arr[2]}',inline=True)
        embed.add_field(name='Total Deaths',value=f'{self.conv(arr[3])}' ,inline=False)
        embed.add_field(name='New Deaths', value=f'{arr[4]}' , inline=True)
        embed.add_field(name='Total Tested', value=f'{self.conv(arr[5])}' , inline=True)

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("😷")
        # print(self.graphd("India"))

    @commands.command(aliases=['list','cl','countries'],help='country name list')
    async def _countries(self,ctx):
        arr = self.country_list()
        text1 = ""
        text2 = ""
        text3 = ""
        for i in range(int(len(arr)/3)):
            text1 = f'{text1} {arr[i]}'
        for j in range(int(len(arr)/3),int(2*len(arr)/3)):
            text2 = f'{text2} {arr[j]}'
        for j in range(int(2*len(arr)/3), int(len(arr))):
            text3 = f'{text3} {arr[j]}'
        await ctx.send(f'```ml\n{text1}\n```')
        await ctx.send(f'```ml\n{text2}\n```')
        await ctx.send(f'```ml\n{text3}\n```')

    @commands.command(aliases=['cvac'])
    async def _vaccine(self,ctx):
        # arr = self.active_cases('india')
        url = 'https://www.mohfw.gov.in/covid_vaccination/vaccination/index.html'
        icmr = 'https://vaccine.icmr.org.in/covid-19-vaccine'
        registration = 'https://www.cowin.gov.in/home'
        embed = discord.Embed(
            title='Vaccination Help', url=url,description='As of now, if your age > 45 then you must get vaccinated\n more details are given below !',color=ctx.author.color)
        embed.set_thumbnail(
            url='https://images.news18.com/ibnlive/uploads/2021/01/1609996706_co-win-app.jpg')
        embed.add_field(name='Covishield', value='The Serum Institute of India (SII) and Indian Council of Medical Research are jointly conducting a Phase II/III, Observer-Blind, Randomized, Controlled Study to Determine the Safety and Immunogenicity of Covishield (COVID-19 Vaccine).',inline=False)
        embed.add_field(name='Covaxin', value="COVAXIN, India's indigenous COVID-19 vaccine Bharat Biotech is developed in collaboration with the Indian Council of Medical Research(ICMR) - National Institute of Virology(NIV). This indigenous, inactivated vaccine is developed and manufactured in Bharat Biotech's BSL-3 (Bio-Safety Level 3) high containment facility.",inline=False)
        embed.add_field(name='Vaccination Details',value=f'[**Register for Vaccination**]({registration})',inline=False)
        embed.set_footer(text=f'For more details on Vaccines [click here]({icmr})')

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("🩺")

    def get_data_by_date(self,country,date,d_short):
        url = "https://covid-193.p.rapidapi.com/history"
        querystring = {"country":country,"day":date}
        headers = {
            'x-rapidapi-key': os.getenv("COVID_BOT_API_KEY"),
            'x-rapidapi-host': "covid-193.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.text    
        res = json.loads(data)
        data = res['response']
        data = data[0]['cases']
        cases_today = []
        cases_today.append(d_short)
        cases_today.append(data['active'])

        cases_today.append(data['recovered'])
        cases_today.append(data['total'])

        return cases_today

    def graphd(self,country):
        chart_cases = [['date','active','recovered','total']]
        today = date.today()
        d1 = datetime.datetime.now()
        arr = [['date','active','recovered','total']]
        for i in range (0,150,15):
            d2 = datetime.timedelta(days = i)
            d2 = d1 - d2
            d_form = d2.strftime("%Y-%m-%d")
            d_short = d2.strftime("%d %b")
            x = self.get_data_by_date(country,d_form,d_short)
            chart_cases.append(x)
        n = len(chart_cases)
        for i in range (n-1):
            arr.append(chart_cases[n-i-1])
        return arr
    
    @commands.command(name="graph")
    async def graphscov(self,ctx,*args):
        data_stream = io.BytesIO()
        country=str(args[0])
        statsss=self.graphd(country)
        activestats=[]
        rstats=[]
        tstats=[]
        dstats=[]
        for stats in statsss:
            activestats.append(stats[1])

            rstats.append(stats[2])

            tstats.append(stats[3])

            dstats.append(stats[0])

        activestats=activestats[1:]
        rstats=rstats[1:]
        tstats=tstats[1:]
        dstats=dstats[1:]

        fig, ax = plt.subplots()
        ax.plot(dstats,activestats,label="Active Cases")
        ax.plot(dstats,rstats,label="Recovered Cases")
        ax.plot(dstats,tstats,label="Total Cases")
        plt.xlabel("Date")
        plt.ylabel("Cases")
        plt.title(f"Stats for {country}")
        plt.tight_layout()
        
        # plt.fill_between(dstats,activestats)
        # plt.show()
        plt.savefig(data_stream, format='jpg', dpi = 80)
        plt.close()
        data_stream.seek(0)
        chart = discord.File(data_stream,filename=f"{country}.jpg")
        embed=discord.Embed(title=f"Here are the latest stats for {country}!")
        embed.set_image(url=f"attachment://{country}.jpg")
        await ctx.message.add_reaction("📊")
        embed.add_field(name="Legend",value="```yaml\nGreen: Total Cases```\n```arm\nOrange: Recovered Cases```\n```md\n#Blue: Active Cases```")
        await ctx.send(embed=embed,file=chart)
        data_stream.truncate(0)
        data_stream.close()
        plt.clf()

    
def setup(client):
    client.add_cog(News(client))
