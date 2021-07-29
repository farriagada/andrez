import os, discord, random, gifFromPGN, json, io
from dotenv import load_dotenv
from discord.ext import tasks, commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
eco_letters = ["A","B","C","D","E"] # Needed to randomly create an ECO value. 
seen_openings = [] # This list is used for checking whether an opening has been recently shown. 

bot = commands.Bot(command_prefix='ob!', description='Daily Opening Bot')

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print( # For logging purposes only. 
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
@client.event    
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == 'ob!Hello':
        response = "Hi, I'm the daily chess opening bot!"
        await message.channel.send(response)
    if message.content == 'ob!Opening':
        found = False
        #Need to wrap this up in a while loop. 
        randeco = random.choice(eco_letters) + "%02d" % random.randint(0,99) # Random ECO from A00 to E99. 
        for op in seen_openings: # Iter through list to check if the ECO has been sent before. 
            if randeco == op:
                found = True
        if found == False: # If it has never been sent, then iter through every opening with that ECO. 
            seen_openings.append(randeco) #Append the ECO to the list so it's remembered. 
            with open('database.json', 'r+') as f:
                openings = json.load(f)
                for opening in openings:
                    if opening['eco'] == randeco: # If we have a match we send the gif. We should have more than one in some cases. 
                        gifFromPGN.getGIF(opening['pgn'])
                        await message.channel.send("**{}**: *{}*".format(opening['eco'], opening['name']), file=discord.File('tmp.gif'))
                        os.remove('tmp.gif')
            f.close()

# Scheduling one ECO Opening a day.                         
@tasks.loop(hours=24)
async def daily_opening(ctx):
    found = False
    randeco = random.choice(eco_letters) + "%02d" % random.randint(0,99) # Random ECO from A00 to E99. 
    for op in seen_openings: # Iter through list to check if the ECO has been sent before. 
        if randeco == op:
            found = True
            break
        if found == False: # If it has never been sent, then iter through every opening with that ECO. 
            seen_openings.append(randeco) #Append the ECO to the list so it's remembered. 
            with open('database.json', 'r+') as f:
                openings = json.load(f)
                for opening in openings:
                    if opening['eco'] == randeco: # If we have a match we send the gif. We should have more than one in some cases. 
                        gifFromPGN.getGIF(opening['pgn'])
                        await ctx.send("**{}**: *{}*".format(opening['eco'], opening['name']), file=discord.File('tmp.gif'))
                        os.remove('tmp.gif')
            f.close()


        
client.run(TOKEN)