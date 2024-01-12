import firebase
import AIClasses


baseprompt1 = firebase.RetrieveFirebase("/vallaut21%3A42%3A24")
settings1 = AIClasses.settings()
HumanPrompt1 = 'What About Detroit?'
Logs =  AIClasses.AIResponse(baseprompt1(), HumanPrompt1, settings1)
print(Logs)
Response = Logs['output']['choices'][0]['text']
print(Response)