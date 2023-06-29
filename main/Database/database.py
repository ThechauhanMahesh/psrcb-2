#Tg:ChauhanMahesh/DroneBots
#Github.com/vasusen-code
import datetime
import motor.motor_asyncio
from .. import MONGODB_URI

SESSION_NAME = 'DemoSRCB'

class Database:
  
#Connection--------------------------------------------------------------------

    def __init__(self, MONGODB_URI, SESSION_NAME):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.db = self._client[SESSION_NAME]
        self.col = self.db.users
        self.expired = []
      
#collection handling---------------------------------------------------------

    def new_user(self, id):
        return dict(
          id=id, 
          banned=False, 
          api_id=None, 
          api_hash=None, 
          session=None, 
          chat=None, 
          process={"process":False, "batch":False}, 
          data={"dos":None, "doe":None, "plan":"basic"},
          trials=0,
          number=0,
        )
           
    async def add_user(self,id):
        user = self.new_user(id)
        await self.col.insert_one(user)
      
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def banning(self, id):
        await self.col.update_one({'id': id}, {'$set': {'banned': True}})
    
    async def is_banned(self, id):
        user = await self.col.find_one({'id': int(id)})
        banned = user.get('banned', False)
        return banned
      
    async def unbanning(self, id):
        await self.col.update_one({'id': id}, {'$set': {'banned': False}})
        
    async def get_users(self):
        users = self.col.find({})
        return users
    
    async def update_session(self, id, session):
        await self.col.update_one({'id': id}, {'$set': {'session': session}})
    
    async def rem_session(self, id):
        await self.col.update_one({'id': id}, {'$set': {'session': None}})
   
    async def update_api_id(self, id, api_id):
        await self.col.update_one({'id': id}, {'$set': {'api_id': api_id}})
    
    async def rem_api_id(self, id):
        await self.col.update_one({'id': id}, {'$set': {'api_id': None}})
        
    async def update_api_hash(self, id, api_hash):
        await self.col.update_one({'id': id}, {'$set': {'api_hash': api_hash}})
    
    async def rem_api_hash(self, id):
        await self.col.update_one({'id': id}, {'$set': {'api_hash': None}})
      
    async def update_number(self, id, number):
        await self.col.update_one({'id': id}, {'$set': {'number': number}})
    
    async def update_chat(self, id, chat):
        await self.col.update_one({'id': id}, {'$set': {'chat': chat}})
    
    async def rem_chat(self, id, sender):
        await self.col.update_one({'id': id}, {'$set': {'chat': sender}})
    
    async def update_data(self, id, data):
        await self.col.update_one({'id': id}, {'$set': {'data': data}})
       
    async def rem_data(self, id):
        await self.col.update_one({'id': id}, {'$set': {'data': {"dos":None, "doe":None, "plan":"basic"}}})
    
    async def update_process(self, id, batch=False):
        await self.col.update_one({'id': id}, {'$set': {'process': {"process":True, "batch":batch}}})
    
    async def rem_process(self, id):
        await self.col.update_one({'id': id}, {'$set': {'process': {"process":False, "batch":False}}})

    async def update_trial_count(self, id):
        user = await self.col.find_one({'id':int(id)})
        trial = user.get('trials', None)
        await self.col.update_one({'id': id}, {'$set': {'trials': trial+1}})
    
    async def get_credentials(self, id):
        user = await self.col.find_one({'id':int(id)})
        i = user.get('api_id', None)
        h = user.get('api_hash', None)
        s = user.get('session', None)
        return i, h, s 

    async def get_chat(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('chat', None)

    async def get_trial_count(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('trials', None)
      
    async def get_data(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('data', None)
      
    async def get_process(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('process', None)

    async def check_number(self, id):
         user = await self.col.find_one({'id':int(id)})
         number = user.get('number', None)
         if number in self.expired:
             return False
         else:
             return True
         
    async def black_list_number(self, id):
        user = await self.col.find_one({'id':int(id)})
        number = user.get('number', None)
        self.expired.append(number)
      
db = Database(MONGODB_URI, SESSION_NAME)
