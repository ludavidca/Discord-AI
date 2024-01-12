import discord
import AIClasses
import firebase
import Translation
import json

discordtoken = json.load(open("discordtoken.json","r"))['key']

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)
#client = class(type), accessing discord through python


#decorator used to describe python to do smth special with the function
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}') #f is format

@client.event
async def on_message(message):
    #try: 
    if message.author == client.user: #if person sent message is bot itself return nothing
        return

    elif message.content.startswith('!Help'):
        await message.channel.send("Send a message starting with ! to talk to the AI")
    
    elif message.content.startswith('!') or message.content.startswith('！'):
        if 'reply' in str(message):  
            ConvoID = (await message.channel.fetch_message(message.reference.message_id)).content.split("[")[-1][:-1]
            PreviousPrompt = firebase.RetrieveFirebase(ConvoID)()
            settings1 = AIClasses.settings()
            HumanPrompt1 = message.content[1:]
            Language = Translation.language(HumanPrompt1)
            if Language == "en":
                Logs =  AIClasses.AIResponse(PreviousPrompt, HumanPrompt1, settings1)
                Reference = firebase.EditFirebase(ConvoID, Logs.get('prompt')[0] ,Logs['output']['choices'][0]['text'])() #add to logs
                Response = AIClasses.sendresponses(Logs['output']['choices'][0]['text'])
                for i in Response:  
                    i.strip("\n")
                    i += f"\n[{str(ConvoID)}]"
                    await message.channel.send(i)
            else:
                transhumanprompt = Translation.translate(HumanPrompt1)
                Logs =  AIClasses.AIResponse(PreviousPrompt, transhumanprompt, settings1)
                Reference = firebase.EditFirebase(ConvoID, Logs.get('prompt')[0] ,Logs['output']['choices'][0]['text'])() #add to logs
                Response = Translation.translate(Logs['output']['choices'][0]['text'], Language)
                Response = AIClasses.sendresponses(Response)
                for i in Response:  
                    i.strip("\n")
                    i += f"\n[{str(ConvoID)}]"
                    await message.channel.send(i)
        else:
            baseprompt1 = AIClasses.basePrompt("Sam Wellington")
            settings1 = AIClasses.settings()
            HumanPrompt1 = message.content[1:]
            Language = Translation.language(str(HumanPrompt1))
            if Language == "en":
                Logs =  AIClasses.AIResponse(baseprompt1(), HumanPrompt1, settings1)
                Reference = firebase.AddFirebase(str(message.author),Logs)() #add to logs
                print(Logs)
                Response = (Logs['output']['choices'][0]['text'])
                Response = AIClasses.sendresponses(Logs['output']['choices'][0]['text'])
                for i in Response:  
                    i.strip("\n")
                    i += f"\n[{str(Reference)}]"
                    await message.channel.send(i)
            else:
                transhumanprompt = Translation.translate(HumanPrompt1)
                Logs =  AIClasses.AIResponse(baseprompt1(), transhumanprompt, settings1)
                Reference = firebase.AddFirebase(str(message.author),Logs)() #add to logs
                Response = Translation.translate(Logs['output']['choices'][0]['text'], Language)
                Response = AIClasses.sendresponses(Response)
                for i in Response:  
                    i.strip("\n")
                    i += f"\n[{str(Reference)}]"
                    await message.channel.send(i)

        
client.run(discordtoken)


