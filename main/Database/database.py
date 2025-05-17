#Tg:ChauhanMahesh/DroneBots
#Github.com/vasusen-code
import asyncio
import datetime
import time
import motor.motor_asyncio
from .. import MONGODB_URI, SESSION_NAME, DUMP_CHANNEL
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class Database:
  
#Connection--------------------------------------------------------------------

    def __init__(self, MONGODB_URI, SESSION_NAME):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.db = self._client[SESSION_NAME]
        self.col = self.db.users
        self.cache = self.db[f"cache_{DUMP_CHANNEL}"]

#collection handling---------------------------------------------------------

    def new_user(self, id):
        return dict(
          id=id, 
          banned=False, 
          api_id=None, 
          api_hash=None, 
          session=None, 
          chat=None, 
          process={"process":False, "last":0, "used":0}, 
          data={"dos":None, "doe":None, "plan":"free"},
          caption={"action":None, "string":None},
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
   
    async def update_chat(self, id, chat):
        await self.col.update_one({'id': id}, {'$set': {'chat': chat}})
    
    async def rem_chat(self, id, sender):
        await self.col.update_one({'id': id}, {'$set': {'chat': sender}})
    
    async def update_data(self, id, data):
        await self.col.update_one({'id': id}, {'$set': {'data': data}})
       
    async def rem_data(self, id):
        await self.col.update_one({'id': id}, {'$set': {'data': {"dos":None, "doe":None, "plan":"basic"}}})
    
    async def update_process(self, id):
        await self.col.update_one({'id': id}, {'$set': {'process': {"process":True}}, "$inc": {"process.used": 1}})
    
    async def rem_process(self, id):
        await self.col.update_one({'id': id}, {'$set': {'process': {"process":False, "last": time.time()}}})

    async def add_caption(self, id, string):
        await self.col.update_one({'id': id}, {'$set': {'caption': {"action":"add", "string":string}}})

    async def delete_caption(self, id, string):
        await self.col.update_one({'id': id}, {'$set': {'caption': {"action":"delete", "string":string}}})

    async def replace_caption(self, id, string):
        await self.col.update_one({'id': id}, {'$set': {'caption': {"action":"replace", "string":string}}})

    async def disable_caption(self, id):
        await self.col.update_one({'id': id}, {'$set': {'caption': {"action":None, "string":None}}})
      
    async def get_credentials(self, id):
        user = await self.col.find_one({'id':int(id)})
        i = user.get('api_id', None)
        h = user.get('api_hash', None)
        s = user.get('session', None)
        return i, h, s 

    async def get_chat(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('chat', None)
      
    async def get_data(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('data', None)

    async def get_process(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('process', None)

    async def get_caption(self, id):
        user = await self.col.find_one({'id':int(id)})
        return user.get('caption', None)
    
    async def save_cache(self, msg_id, chat_id, cache_msg_id, caption=""):
        try:
            await self.cache.insert_one({"_id": f"{msg_id}_{chat_id}", "msg_id": cache_msg_id, "caption": caption})
        except:
            pass
    
    async def get_cache(self, msg_id, chat_id) -> int | None:
        cache = await self.cache.find_one({"_id": f"{msg_id}_{chat_id}"})
        return cache if cache else {}
    
    async def reset_free_limits(self):
        await self.col.update_many(
                {"data.plan": "free"},
                {'$set': {
                    'process.used': 0,
                    'process.process': False
                }}
            )

    async def restart_bot(self):
        await self.col.update_many(
                {},
                {'$set': {
                    'process.process': False,
                }}
            )

db = Database(MONGODB_URI, SESSION_NAME)

#Reset processes at startup
asyncio.run(db.restart_bot())
#Scheduler--------------------------------------------------------------------
#Scheduler to reset free limits at 00:00 IST
scheduler = AsyncIOScheduler(tz="Asia/Kolkata")
scheduler.add_job(db.reset_free_limits, "cron", hour=0)
scheduler.start()