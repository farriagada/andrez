import os, discord, random, gifFromPGN, json, requests
from dotenv import load_dotenv
from discord.ext import tasks


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
LICHESSTOKEN = os.getenv('LICHESS_TOKEN')

client = discord.Client()
eco_letters = ["A","B","C","D","E"] # Needed to randomly create an ECO value. 
seen_openings = [] # This list is used for checking whether an opening has been recently shown. 

@client.event
async def on_ready():
    daily_opening.start() # Start looping the daily opening task.
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
    # This module doesn't work because gifs are apparently heavier than what discord accepts. 
    # The coding is right, though. 
    if message.content.startswith('https://lichess.org/'):
        try:
            # First, we get whatever is after /. 
            splittedlist = message.content.rsplit('/',1)
            auth = {"Authorization": "Bearer {}".format(LICHESSTOKEN)}
            myurl = 'https://lichess.org/game/export/{}'.format(splittedlist[1])
            print("this is what I'm sending: {}".format(myurl))
            r = requests.get(myurl, headers=auth)
            if str(r.content.decode('utf-8')).startswith('<!DOCTYPE html>'):
                print('This link is not a Lichess game.')
            else:
                gifFromPGN.getBiGif(r.content.decode('utf-8'))
                await message.channel.send('Great game!', file=discord.File('tmp.gif'))
                os.remove('tmp.gif')
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    if message.content == 'adz!Hello':
        response = "Hi, I'm the daily chess opening bot!"
        await message.channel.send(response)
    if message.content == 'adz!Opening':
        #Need to wrap this up in a while loop. 
        randeco = random.choice(eco_letters) + "%02d" % random.randint(0,99) # Random ECO from A00 to E99. 
        with open('database.json', 'r+') as f:
            openings = json.load(f)
            for opening in openings:
                if opening['eco'] == randeco: # If we have a match we send the gif. We should have more than one in some cases. 
                    gifFromPGN.getGIF(opening['pgn'])
                    await message.channel.send("**{}**: *{}*".format(opening['eco'], opening['name']), file=discord.File('tmp.gif'))
                    os.remove('tmp.gif')
                    break # We break loop to avoid sending more than one opening. 
                 
        f.close()
    # COMMAND FOR CLEARING ECO FILE CACHE FOR OPENINGS #
    if message.content == 'a!clear_cache':
      with open('seen_openings', 'r+') as f:
          f.truncate(0)
          print("Seen ECO codes file cleared successfully!")
          f.close()



# Scheduling one ECO Opening a day.                         
@tasks.loop(hours=24)
async def daily_opening():
    chnl = client.get_channel(870427640601923655) # This is for general channel on my guild. Upgrade if we want to make the bot public. 
    found = False
    randeco = random.choice(eco_letters) + "%02d" % random.randint(0,99) # Random ECO from A00 to E99. 
    with open('seen_openings', 'r+') as o:
        for eco in o: # Iter through list to check if the ECO has been sent before. 
            if randeco == eco:
                found = True
                break
    o.close()
    if found == False: # If it has never been sent, then iter through every opening with that ECO. 
        with open('seen_openings', "a") as ow:
            ow.write('{}\n'.format(randeco)) #Append the ECO to the list so it's remembered.
            ow.close() 
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