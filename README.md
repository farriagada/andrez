# Andrez, a simple and lightweight chess discord bot!

Hi, I'm **Andrez**, a simple chess bot that will post a daily chess opening CHESS for you to study. I'm still in beta testing so you're gonna have to install me manually in order for me to work.  


## How to install me

The code here is working, but it needs a couple things for you to change so I can live within your own discord guild. Here are the steps:

 1. First of all, you should clone this project in whatever folder you want it to run. 
 2. I'm taking for granted that you know how to create a Discord project and a bot. You should have both ready to use by now. 
 3. Open the .env file and change those three values with your own!
    `DISCORD_TOKEN= Your secret guild token goes here`
`DISCORD_GUILD= Your guild name goes here`
`LICHESS_TOKEN= You should create a lichess token and put it here, for future use`

 4. Go into andrez.py and change the channel ID (line 78) with the ID of the channel you want me to post the daily opening.  
 5. Run `python3 andrez.py` and that's it! You now have me running in your guild!

## Next Steps

I'm currently working into new skills for me to dazzle you and your friends. For instance, I'm soon gonna be able to GIF up every Lichess game link you share into discord, so your friends can watch a preview of that game before they even click the link! 

I'm also refactoring myself so I'm no longer a personal project. Soon I'll be able to work in every guild with just one click! 

If you have any feedback or idea I'll be looking forward to hearing it! 
