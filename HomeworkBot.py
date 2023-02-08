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

def getNextWkDay():
    year = datetime.now().year
    today = datetime(year, datetime.now().month, datetime.now().day)
    wkDay = today.strftime('%a')
    if today.strftime('%a') == 'Fri':
        nextWkDay = today+timedelta(days=3)
    elif today.strftime('%a') == 'Sat':
        nextWkDay = today+timedelta(days=2)
    else:
        nextWkDay = today+timedelta(days=1)
    return nextWkDay


fullRole=f'<@&{1067180148702593135}>'

def SendMessage():
    global homework
    LoadJSON()

    dueNextWkDay=[]
    dueAfter=[]
    year=datetime.now().year
    today=datetime(year,datetime.now().month,datetime.now().day)
    tomorow=today+timedelta(days=1)
    nextWkDay = getNextWkDay()
    modifier=0

    for i in range(len(homework)):
        curI=homework[i-modifier]
        due=datetime(year,int(curI["dueMonth"]),int(curI["dueDay"]))
        
        subject=names[curI["subject"]]
        if due == nextWkDay:
            dueNextWkDay.append(f"> **{subject}** {curI['txt']}")
        elif due < tomorow:
            homework.pop(i-modifier)
            modifier+=1
        else:
            dueAfter.append(f"> `{int(curI['dueDay']):02}/{int(curI['dueMonth']):02}` **{subject}** {curI['txt']}")
        
    SaveJSON()

    message=f'{fullRole} due {nextWkDay.strftime("%A, %d %b")}:\n'
    if len(dueNextWkDay)==0:
        message=f'{message}> None\n'
    for hwItem in dueNextWkDay:
        message=f'{message}{hwItem}\n'
    if len(dueAfter)>0:
        message=f'{message}\nOther homework due:\n'
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
    LoadJSON()

    added = added.split(',',2)
    print(added)
    tDate = added[0].split('/')
    print(tDate)

    year=datetime.now().year
    try:
        tmp = datetime(year,int(tDate[1]),int(tDate[0]))
        goodDate = True
    except:
        goodDate = False

    if len(added) != 3 or len(tDate) != 2:
        await ctx.send("**Error**: Please add with the following format. `day/month, subject, task`")
    elif added[1].strip() not in names:
        await ctx.send("**Error**: Please enter a valid **subject** with the following format. `day/month, subject, task` For more info see `!help subjects`.")
    elif not goodDate:
        await ctx.send("**Error**: Please enter a valid **date** with the following format. `*day/month*, subject, task`")
    elif datetime(year,int(tDate[1]),int(tDate[0])) < datetime(datetime.now().year,datetime.now().month,datetime.now().day)+timedelta(days=1):
        await ctx.send("**Error**: Please enter a valid **date** that is **after today** with the following format. `*day/month*, subject, task`")
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
    nextWkDay = getNextWkDay()
    nWkDShort = nextWkDay.strftime("%d/%m")
    nWkDLong = nextWkDay.strftime("%d of %b").lstrip("0")
    msg = SendMessage().replace(fullRole,'<Role>')
    embed = discord.Embed(title = "Homework", description = msg)
    await ctx.send(embed = embed)

#help commadnds
client.remove_command('help')
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Help", description="Use !help <command> for more info")

    embed.add_field(name='Adding Hw', value='`add`')
    embed.add_field(name='Subject Keys', value='`subjects`')
    embed.add_field(name='Checking Hw', value='`test`')
    embed.add_field(name='Sending Hw', value='`send`')

    await ctx.send(embed=embed)

@help.command()
async def add(ctx):
    year=datetime.now().year
    today=datetime(year,datetime.now().month,datetime.now().day)
    nextWkDay = getNextWkDay()
    nWkDShort = nextWkDay.strftime("%d/%m")
    nWkDLong = nextWkDay.strftime("%d of %b").lstrip("0")
    
    #Embed(add)
    embed = discord.Embed(title="Help: Add", description="This command adds items of homework to the list.")

    embed.add_field(name='**Syntax**', value=f'There are 3 parameters:\n> **Date**: Day & Month: `{nWkDShort}`({nWkDLong})\n> **Subject**: Signified by 3/4 letters. Do `!help subjects` for list of subjects.\n> **Task**: E.g. `Scipad pg 222`')

    embed.add_field(name='**Example Usage**', value=f'If you want to add Scipad pg 222 for Science on the {nWkDLong} then you would type: `!add {nWkDShort}, sci, Scipad pg 222`')
    await ctx.send(embed=embed)

#subjects
@help.command()
async def subjects(ctx):
    embed = discord.Embed(title="Help: Subject Codes", description="This command shows all the subject codes used in the add command.")

    embed.add_field(name='**Syntax**', value=f'''
    > Tutor: `tut`
> 
    > Chinese: `chi`
    > Spanish: `spa`
    > 
    > English: `eng`
    > Humanities: `hum`
> 
    > Maths: `mat`
    > Science: `sci`
> 
    > Advanced Maths: `amat`
    > Advanced Science: `asci`
> 
    > Music: `mus`
> 
    > Art: `art`
    ''')
    await ctx.send(embed=embed)


#test
@help.command()
async def test(ctx):
    embed = discord.Embed(title="Help: Test", description="This sends the homework message in the channel you are currently in are removes the ping.")    


#send
@help.command()
async def send(ctx):
    embed = discord.Embed(title="Help: Send", description="This sends the homework message in the homework channel and pings the homework role.")  

#loging messages
@client.event
async def on_message(message):
    with open("log.txt","a") as f:
        f.write(f"Message SENT at {message.created_at} from {message.guild} - {message.channel} by {message.author}: '{message.content}'\n")
    await client.process_commands(message)

@client.event
async def on_message_delete(message):
    with open("log.txt","a") as f:
        f.write(f"Message DELETED at {message.created_at} from {message.guild} - {message.channel} by {message.author}: '{message.content}'\n")
    await client.process_commands(message)

@client.event
async def on_message_edit(message,afterMessage):
    with open("log.txt","a") as f:
        f.write(f"Message CHANGED at {message.created_at} from {message.guild} - {message.channel} by {message.author}: '{message.content} -> {afterMessage.created_at} from {afterMessage.guild} - {afterMessage.channel} by {afterMessage.author}: '{afterMessage.content}'\n")
    await client.process_commands(message)

client.run(TOKEN)