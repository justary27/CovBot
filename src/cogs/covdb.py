import discord
from discord.ext import commands
import sqlite3,json,datetime,gspread

class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

    # def news(self,country):

    @commands.command(aliases=['add'])
    async def test_(self,ctx,*,msg):
        msg = msg.split("/") # message in the form of name;place;contact_no.;leads
        name,state,place,c_no,leads = msg[0],msg[1],msg[2],msg[3],msg[4]
        guild_id = ctx.message.guild.id
        conn = sqlite3.connect('covid_db.db')
        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE uv_guild{}(
                        name text,
                        state text,
                        place text,
                        contact text,
                        lead text,
                        added_by text,
                        date text
                        )""".format(guild_id))
        except:
            print(f"unverifed guild{guild_id} already there !")

        c.execute("INSERT INTO uv_guild{} VALUEs (?,?,?,?,?,?,?)".format(guild_id), (name,state.lower(),place.lower(), c_no, leads.lower(),ctx.author.mention,datetime.date.today()))
        conn.commit()
        conn.close()
        await ctx.send(embed=discord.Embed(description="Added sucessfully !!"))

    @commands.command(aliases=['get'])
    async def get_(self,ctx,type:str=None,*,search:str=None):
        guild_id = ctx.message.guild.id
        info = " "
        conn = sqlite3.connect('covid_db.db')
        c = conn.cursor()
        c.execute("SELECT * FROM v_guild{}".format(guild_id))
        data = c.fetchall()
        # print(data)
        conn.commit()
        conn.close()
        print('searching...')
        if type=='place':
            try:
                for i in range(len(data)):
                    filter = data[i][2].split(',')
                    print(filter)
                    if search.lower() in filter:
                        details = f"> **Name** : {data[i][0].capitalize()}\n>**State**:{data[i][1]}\n> **Place** : {data[i][2]}\n> **Contact** : {data[i][3]}\n> **Leads** : {data[i][4]} \n> **Added by** : {data[i][5]}\n> **Date** : {data[i][6]}"
                        info = f"{info}\n {details}\n"
                await ctx.send(embed=discord.Embed(description=info,color=discord.Color.blue()))
            except:
                await ctx.send(embed=discord.Embed(description=f"There's no lead for **{search}**, add one to see it !",color=discord.Color.red()))
        elif type =='leads' or type=='lead':
            try:
                for i in range(len(data)):
                    if search.lower() in data[i][3]:
                        details = f"> **Name** : {data[i][0].capitalize()}\n>**State**:{data[i][1]}\n> **Place** : {data[i][2]}\n> **Contact** : {data[i][3]}\n> **Leads** : {data[i][4]}\n> **Added by** : {data[i][5]}\n> **Date** : {data[i][6]}"
                        info = f"{info}\n {details}\n"
                await ctx.send(embed=discord.Embed(description=info,color=discord.Color.blue()))
            except:
                await ctx.send(embed=discord.Embed(description=f"There's no lead for **{search}**, add one to see it !",color=discord.Color.red()))

    @commands.command(aliases=['verify'])
    async def verify_(self,ctx,num:int):
        guild_id = ctx.message.guild.id
        conn = sqlite3.connect('covid_db.db')
        c = conn.cursor()
        c.execute("SELECT * FROM uv_guild{}".format(guild_id))
        dict = c.fetchall()
        name,state,place,contact,leads = dict[num-1][0],dict[num-1][1],dict[num-1][2],dict[num-1][3],dict[num-1][4]
        verifier = ctx.author.mention

        print(f'>> Verified {leads}')
        conn.commit()
        try:
            c.execute("""CREATE TABLE v_guild{}(
                        name text,
                        state text,
                        place text,
                        contact text,
                        lead text,
                        added_by text,
                        date text
                        )""".format(guild_id))
        except:
            print(f"unverifed guild{guild_id} already there !")

        c.execute("INSERT INTO v_guild{} VALUEs (?,?,?,?,?,?,?)".format(guild_id),(name,state, place, contact, leads,verifier,datetime.date.today()))
        conn.commit()
        c.execute("DELETE from uv_guild{} WHERE lead='{}'".format(guild_id, leads))
        conn.commit()
        conn.close()
        await ctx.send(embed=discord.Embed(title="Verified Sucessfully !",description=f"> **Leads** : {leads}\n> **Contact** : {contact}\n> Verified by {verifier} at {str(datetime.datetime.now())[:19]} "))

    @commands.command(aliases=['getall'])
    async def get_all(self,ctx,type:str='verified'):
        guild_id = ctx.message.guild.id
        if type.lower() == 'verified' or type == 'v':
            type = f"v_guild{guild_id}"
        elif type.lower()=='unverifed' or type == 'uv':
            type =  f"uv_guild{guild_id}"
        conn = sqlite3.connect('covid_db.db')
        c = conn.cursor()
        info = " "
        c.execute("SELECT * FROM {}".format(type))
        data = c.fetchall()
        for i in range(len(data)-1,-1,-1):
            details = f"> **Name** : {data[i][0].capitalize()}\n> **State** : {data[i][1]}\n> **Adress** : {data[i][2]}\n> **Contact** : {data[i][3]}\n> **Leads** #{i+1}: {data[i][4]}\n> **Added by** : {data[i][5]}\n> **Date** : {data[i][6]}"
            info = f"{info}\n {details}\n"
        if len(info) > 2000:
            info = info[:2000]
        else:
            info = info
        await ctx.send(embed=discord.Embed(description=info,color=discord.Color.blue()))

    @commands.command(aliases=['remove'])
    async def remove_(self,ctx,type:str,num:int):
        guild_id = ctx.message.guild.id
        if type.lower() == 'verified' or type == 'v':
            type = f"v_guild{guild_id}"
        elif type.lower()=='unverifed' or type == 'uv':
            type =  f"uv_guild{guild_id}"
        conn = sqlite3.connect('covid_db.db')
        c = conn.cursor()
        # DELETE IF DOESN'T WORK
        c.execute("SELECT * FROM {}".format(type))
        dict = c.fetchall()
        leads = dict[num - 1][4]
        print(f'>> removed {leads}')
        conn.commit()
        c.execute("DELETE from {} WHERE lead='{}'".format(type, leads))
        conn.commit()
        conn.close()
        await ctx.send(embed=discord.Embed(description=f'Removed Lead: {leads}',color=discord.Color.orange()))

    @commands.command(aliases=['push'])
    async def push_sheet(self,ctx,num:int):
        guild_id = ctx.message.guild.id
        msg = await ctx.send(embed=discord.Embed(description="Adding to google sheets",color=discord.Color.orange()))
        gc = gspread.service_account(filename='credentials.json')
        sh = gc.open('trail')
        worksheet = sh.sheet1
        conn = sqlite3.connect('covid_db.db')
        c = conn.cursor()
        c.execute("SELECT * FROM v_guild{}".format(guild_id))
        dict = c.fetchall()
        user = []
        try:
            for j in range(5):
                user.append(dict[num-1][j])
            user.insert(4,'True')
            worksheet.append_row(user)
            await msg.edit(embed=discord.Embed(description="Pushed to google sheets",color=discord.Color.green()))
        except:
            await msg.edit(embed=discord.Embed(description="Failed to push, Try Again !",color=discord.Color.red()))

    @commands.command(aliases=['pull'])
    async def pull_sheet(self,ctx):
        # SHEET SHOULD BE IN FORMAT OF NAME,STATE,PLACE(CITY),CONTACT,Verified,LEADS
        guild_id = ctx.message.guild.id
        gc  = gspread.service_account(filename='credentials.json')
        sh = gc.open('trail')
        worksheet = sh.sheet1
        res = worksheet.get_all_values()
        conn = sqlite3.connect('covid_db.db')
        c = conn.cursor()
        # print(res)
        for i in range(1,len(res)):

            name,state,place,c_no,leads = res[i][0],res[i][1],res[i][2],res[i][3],res[i][5]
            print(name)
            c.execute("INSERT INTO uv_guild{} VALUEs (?,?,?,?,?,?,?)".format(guild_id), (name,state.lower(),place.lower(), c_no, leads.lower(),ctx.author.mention,datetime.date.today()))
            conn.commit()
        conn.close()
        await ctx.send(embed=discord.Embed(description="Data fetched sucessfully.",color=discord.Color.green()))

def setup(client):
    client.add_cog(Database(client))
