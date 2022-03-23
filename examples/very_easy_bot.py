# import a main namespace
import melisa

# initate a bot`s client
client = melisa.Client(token='your bot token', # you have to get your bot token on https://discord.com/developers/applications
                       intents=melisa.Intents.all() # you have to initiate intents here and in your bot`s application
                       )

# run your bot
client.run()