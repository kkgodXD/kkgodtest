from pymongo import *
from  aiogram import Bot, types
import time
import datetime as Dt
import asyncio

myBot = Bot(token="1779399322:AAG6TLSDv6pEECnFJdpgT77Msfqar9tSkQg")
client = MongoClient('localhost', 27017)
db_obj = client['users_bot_mn']

class K_m:
    def __init__(self, name, chat_id):
        try:
            for el in tuple(db_obj[str(chat_id)].find({}, {'_id' : 0})):
                try:
                    n = float(name[-1])
                    n = 2
                except:
                    n = 1

                if len(name) == n and el['full_name'] == name[0] or el['nickname'] == name[0].replace('@', ''):
                    self.user_id = el['user_id']
                    break
                elif len(name) == n + 1 and el['full_name'] == name[0] + ' ' + name[1]:
                    self.user_id = el['user_id']
                    break
        except:
            pass

    async def check(self, el):
        try:
            lol = float(el)
            return True
        except:
            return False

    async def kick(self, chat_id):
        await myBot.kick_chat_member(chat_id, self.user_id)

    async def ban(self, *mes):
        if len(mes) == 2:
            if await self.check(mes[1].split()[-1]):
                if float(mes[1].split()[-1]) > 525600:
                    await myBot.kick_chat_member(mes[0], self.user_id)

                elif float(mes[1].split()[-1]) <= 525600:
                    await myBot.kick_chat_member(mes[0], self.user_id)
                    await asyncio.sleep(float(mes[1].split()[-1]) * 60)
                    await myBot.unban_chat_member(mes[0], self.user_id)
            else:
                await myBot.kick_chat_member(mes[0], self.user_id)
        else:
            await myBot.kick_chat_member(mes[0], self.user_id)

    async def unban(self, chat_id):
       await myBot.unban_chat_member(chat_id, self.user_id)

    async def mute(self, *mes):
        try:
            if len(mes) == 2:
                if await self.check(mes[1].split()[-1]):
                    if float(mes[1].split()[-1]) < 0.5:
                        await myBot.restrict_chat_member(mes[0], self.user_id, until_date=time.time() + 30)

                    elif float(mes[1].split()[-1]) > 525600:
                        await myBot.restrict_chat_member(mes[0], self.user_id)

                    elif 0.5 <= float(mes[1].split()[-1]) <= 525600:
                        await myBot.restrict_chat_member(mes[0], self.user_id, until_date=time.time() + float(mes[1].split()[-1]) * 60)
                else:
                    await myBot.restrict_chat_member(mes[0], self.user_id)

            else:
                await myBot.restrict_chat_member(mes[0], self.user_id)
        except:
            pass

    async def unmute(self, chat_id):
        await myBot.restrict_chat_member(chat_id, self.user_id, can_send_messages=True,
                                         can_send_other_messages=True, can_send_media_messages=True, can_add_web_page_previews=True)

    async def changeperm(self, com, change_perm):
        try:
            role = tuple(db_obj[str(com.chat.id)].find({'user_id' : self.user_id}, {'role': 1}))[0]['role']
            if com.text.split()[-1] == 'looking':
                if role == 'user':
                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'looking'}})
                    await myBot.send_message(com.chat.id, 'Роль [looking] успешно установлена.')
                    await self.mute(com.chat.id)

                elif role == 'moderator' and change_perm > 1:
                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'looking'}})
                    await myBot.send_message(com.chat.id, 'Роль [looking] успешно установлена.')
                    await self.mute(com.chat.id)

                elif role == 'admin' and change_perm == 3:
                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'looking'}})
                    await myBot.send_message(com.chat.id, 'Роль [looking] успешно установлена.')
                    await self.mute(com.chat.id)

            elif com.text.split()[-1] == 'user':
                if role == 'looking':

                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'user'}})
                    await myBot.send_message(com.chat.id, 'Роль [user] успешно установлена.')
                    await self.unmute(com.chat.id)

                elif role == 'moderator' and change_perm > 1:

                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'user'}})
                    await myBot.send_message(com.chat.id, 'Роль [user] успешно установлена.')

                elif role == 'admin' and change_perm == 3:

                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'user'}})
                    await myBot.send_message(com.chat.id, 'Роль [user] успешно установлена.')

            elif com.text.split()[-1] == 'admin' and change_perm == 3:

                db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'admin'}})
                await myBot.send_message(com.chat.id, 'Роль [admin] успешно установлена.')
                if role == 'looking':
                    await self.unmute(com.chat.id)


            elif com.text.split()[-1] == 'moderator':
                if role == 'admin' and change_perm == 3:

                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'moderator'}})
                    await myBot.send_message(com.chat.id, 'Роль [moderator] успешно установлена.')

                elif role == 'user' and change_perm > 1:

                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'moderator'}})
                    await myBot.send_message(com.chat.id, 'Роль [moderator] успешно установлена.')

                elif role == 'looking' and change_perm > 1:

                    db_obj[str(com.chat.id)].update_one({'user_id' : self.user_id}, {'$set' : {'role': 'moderator'}})
                    await myBot.send_message(com.chat.id, 'Роль [moderator] успешно установлена.')
                    await self.unmute(com.chat.id)

        except:
            pass