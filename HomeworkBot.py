import os
import discord
import json
from datetime import datetime
from datetime import timedelta
from discord.ext import commands

names={
    "tut":'Tutor',

    "chi":'Chinese',
    "spa":'Spanish',
    "eng":'English',
    "hum":'Humanities',

    "mat":'Maths',
    "amat":'Advanced Maths',
    "sci":'Science',
    "asci":'Advanced Science',

    "mus":'Music',
    "art":'Art',
}

fileName = 'homework.json'
def SaveJSON():
    importedJson=open(fileName,"w")
    importedJson.write(json.dumps(homework))
    importedJson.close()

def LoadJSON():
    global homework
    fileName="homework.json"
    importedJson=open(fileName,"r")
    homework=json.loads(importedJson.read())
    importedJson.close()

fullRole=f'<@&{1067180148702593135}>'

def SendMessage():
    global homework
    LoadJSON()

    dueTomorow=[]
    dueAfter=[]
    year=datetime.now().year
    today=datetime(year,datetime.now().month,datetime.now().day)
    tomorow=today+timedelta(days=1)
    modifier=0

    for i in range(len(homework)):
        curI=homework[i-modifier]
        due=datetime(year,int(curI["dueMonth"]),int(curI["dueDay"]))
        subject=names[curI["subject"]]
        if due==tomorow:
            dueTomorow.append(f"> **{subject}** {curI['txt']}")
        elif due>tomorow:
            dueAfter.append(f"> `{int(curI['dueDay']):02}/{int(curI['dueMonth']):02}` **{subject}** {curI['txt']}")
        else:
            homework.pop(i)
            modifier+=1
    
    SaveJSON()

    message=f'{fullRole} due {tomorow.strftime("%A, %d %b %Y")}:\n'
    if len(dueTomorow)==0:
        message=f'{message}> None\n'
    for hwItem in dueTomorow:
        message=f'{message}{hwItem}\n'
    if len(dueAfter)>0:
        message=f'{message}\nHomework due after {tomorow.strftime("%A, %d %b %Y")}:\n'
        for hwItem in dueAfter:
            message=f'{message}{hwItem}\n'
    message=f'{message}\nPlease message me if I have missed something and put questions in the <#1068030623610052638>.'
    return message

f = open('.env')
TOKEN = f.readline()
GUILD = f.readline()

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.command()
async def add(ctx, *, added):
    added = added.split(',')
    print(added)
    tDate = added[0].split('/')
    print(tDate)
    year=datetime.now().year
    today=datetime(year,datetime.now().month,datetime.now().day)
    tomorow=today+timedelta(days=1)
    modifier=0

    LoadJSON()

    if len(added) != 3 or len(tDate) != 2:
        await ctx.send("**Error**: Please add with the following format. `day/month, subject, task`")
    else:
        homework.append({})
        homework[-1]['subject'] = added[1].strip()
        homework[-1]['txt'] = added[2].strip()
        homework[-1]['dueDay'],homework[-1]['dueMonth'] = tDate
        SaveJSON()

#send hw
@client.command()
async def send(ctx):
    channel=client.get_channel(1067180194537930844)
    await channel.send(embed = discord.Embed(title="Homework", description=SendMessage()))

#send hw
@client.command()
async def test(ctx):
    channel=client.get_channel(1067180194537930844)
    msg = SendMessage().replace(fullRole,'<Role>')
    embed = discord.Embed(title = "Homework", description = msg)
    await ctx.send(embed = embed)

#help commadnds
client.remove_command('help')
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Help", description="Use !help <command> for more info")

    embed.add_field(name='Adding Hw', value='`add`')
    embed.add_field(name='Sending Hw', value='`send/test`')

    await ctx.send(embed=embed)

@help.command()
async def add(ctx):
    embed = discord.Embed(title="Help: Add", description="This command adds items of homework to the list.")

    embed.add_field(name='**Syntax**', value='There are 3 parameters:\n> Date: Day & Month: `9/2`(9th of Feb)\n\n> Subject: Signified by 3/4 letters. Do !help subjects for list of subjects.\n\n> Task: E.g. `Scipad pg 222`')

    embed.add_field(name='**Example Usage**', value='If you want to add Scipad pg 222 for Science on the 9th of Feb then you would type: `!add 9/2, sci, Scipad pg 222')
    await ctx.send(embed=embed)


client.run(TOKEN)