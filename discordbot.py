import os, discord, random, gifFromPGN, json

from discord.ext.commands.context import Context
from dotenv import load_dotenv
from discord.ext import tasks


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
eco_letters = ["A","B","C","D","E"] # Needed to randomly create an ECO value. 
seen_openings = [] # This list is used for checking whether an opening has been recently shown. 

@client.event
async def on_ready():
    daily_opening.start() # Start looping.
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print( # For logging purposes only. 
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event    
async def on_message(message): # The main difference is that we only get one per request.  
    if message.author == client.user:
        return
    if message.content == 'ob!Hello':
        response = "Hi, I'm the daily chess opening bot!"
        await message.channel.send(response)
    if message.content == 'ob!Opening':
        #Need to wrap this up in a while loop. 
        randeco = random.choice(eco_letters) + "%02d" % random.randint(0,99) # Random ECO from A00 to E99. 
        with open('database.json', 'r+') as f:
            openings = json.load(f)
            for opening in openings:
                if opening['eco'] == randeco: # If we have a match we send the gif. We should have more than one in some cases. 
                    gifFromPGN.getGIF(opening['pgn'])
                    await message.channel.send("**{}**: *{}*".format(opening['eco'], opening['name']), file=discord.File('tmp.gif'))
                    os.remove('tmp.gif')
                    break # We break loop to avoid sending more than one opening. This should be upgraded. 
        f.close()

# Scheduling one ECO Opening a day.                         
@tasks.loop(hours=24)
async def daily_opening():
    chnl = client.get_channel(867866114674393140)
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
                    gifFromPGN.getGIF(opening['pgn']) # We get the GIF
                    await chnl.send("**{}**: *{}*".format(opening['eco'], opening['name']), file=discord.File('tmp.gif')) # We post the GIF in the channel. 
                    os.remove('tmp.gif') # We delete the GIF. 
                    print("Created GIF for {} opening (ECO code {})".format(opening['name'], opening['eco']))
        f.close()

client.run(TOKEN)