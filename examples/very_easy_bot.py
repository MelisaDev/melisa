import melisa

token = 'ODg3MzU0NjA3Njc4OTI2ODQ4.YUC7YA.3KEjLpaoGYN7lgy0GmQm-gATd1A'

client = melisa.Client(token=token, intents=melisa.Intents.all())

client.run()