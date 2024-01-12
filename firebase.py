from datetime import datetime
import firebase_admin
from firebase_admin import db
from firebase_admin import credentials

cred = credentials.Certificate('secretkey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://discordailogs-default-rtdb.firebaseio.com"
})

class AddFirebase:
    def __init__(self, username, conversation):
        self.username = username
        self.conversation = conversation

    def __call__(self):
        now = datetime.now().strftime("%H:%M:%S")
        reference = f"{self.username}{now}"
        users_ref = db.reference(reference)
        information = str(self.conversation['prompt'][0])+"\n\n"+str(self.conversation['output']['choices'][0]['text'])
        users_ref.set(information)
        return(reference)
        
        

class RetrieveFirebase:
    def __init__(self, reference):
        self.reference = reference

    def __call__(self):
        ref = db.reference(self.reference)
        data = ref.get()
        return data

class EditFirebase:
    def __init__(self, reference, NewConvo, NewReply):
        self.reference = reference
        self.NewConvo = NewConvo
        self.NewReply = NewReply

    def __call__(self):
        ref = db.reference(self.reference)
        ref.set(self.NewConvo + self.NewReply)
