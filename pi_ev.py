from  aiogram import Bot
import time
import datetime as Dt
import asyncio

myBot = Bot(token="1779399322:AAG6TLSDv6pEECnFJdpgT77Msfqar9tSkQg")

class Pin_ev:
    zakreps_dict = dict()
    events_dict = dict()
    numb = 1

    async def is_cheker(self, mes, ev_v):
        for el in ev_v:
            if mes in el:
                return True

    async def event_timer(self, chat_id, info, n):
        if len(info) == 3:
            dt = Dt.datetime.strptime(f"{info[1]} {info[2]}", '%d.%m.%Y %H:%M').timestamp()
            if 60 <= dt - time.time() <= 3600:
                wait_time = (dt - time.time()) / 3
                await asyncio.sleep(dt - time.time() - wait_time)
                await myBot.send_message(chat_id, f"Скоро событие!\n{info[0]}\nВ {info[2]}")
            elif 3600 < dt - time.time() <= 86400:
                wait_time = dt - time.time() - 3600
                await asyncio.sleep(dt - time.time() - wait_time)
                await myBot.send_message(chat_id, f"Событие через час!\n{info[0]}\nВ {info[2]}")
            else:
                wait_time = dt - time.time() - 86400
                await asyncio.sleep(dt - time.time() - wait_time)
                await myBot.send_message(chat_id, f"Уже завтра событие!\n{info[0]}\nВ {info[2]}")
                wait_time = dt - time.time() - 3600
                await asyncio.sleep(dt - time.time() - wait_time)
                await myBot.send_message(chat_id, f"Событие через час!\n{info[0]}\nВ {info[2]}")

        elif len(info) == 2 and len(info[1]) == 4 or len(info[1]) == 5:
            dt = Dt.datetime.strptime(f"{Dt.datetime.now().date()} {info[1]}", "%Y-%m-%d %H:%M").timestamp()
            if 60 <= dt - time.time() <= 3600:
                wait_time = (dt - time.time()) / 3
                await asyncio.sleep(dt - time.time() - wait_time)
                await myBot.send_message(chat_id, f"Скоро событие!\n{info[0]}\nВ {info[1]}")

            elif 3600 < dt - time.time() < 86400:
                wait_time = dt - time.time() - 3600
                await asyncio.sleep(dt - time.time() - wait_time)
                await myBot.send_message(chat_id, f"Событие через час!\n{info[0]}\nВ {info[1]}")

        elif len(info) == 2 and len(info[1]) == 10:
            dt = Dt.datetime.strptime(f"{info[1]} 00:00", "%d.%m.%Y %H:%M").timestamp()
            if dt > 7200:
                await asyncio.sleep(dt - time.time() - 7200)
            else:
                await asyncio.sleep((dt - time.time()) / 2)
            await myBot.send_message(chat_id, f"Уже завтра!\n{info[0]}")

        await asyncio.sleep(dt - time.time())
        del self.events_dict[chat_id][n]
        self.numb -= 1

    async def pinup(self, com):
        if not com.chat.id in self.zakreps_dict.keys():
            self.zakreps_dict.update({com.chat.id : list()})
        self.zakreps_dict[com.chat.id].append(com.reply_to_message.text)

    async def denup(self, com):
        for i in com.text.split()[1:]:
            try:
                if int(i)> 0:
                    try:
                        del self.zakreps_dict[com.chat.id][int(i) - 1]
                    except:
                        del self.zakreps_dict[com.chat.id][-1]
            except:
                pass

    async def pinups(self, com):
        pinups = ""
        for el in self.zakreps_dict[com.chat.id]:
            pinups += f"●  {el}\n\n"

        if pinups == "":
            await myBot.send_message(com.chat.id, "Закрепленных сообщений нет(")
        else:
            await myBot.send_message(com.chat.id, f"Закрепленные сообщения:\n{pinups}")

    async def event(self, com):
        if not com.chat.id in self.events_dict.keys():
            self.events_dict.update({com.chat.id : dict()})

        if len(com.text.split()) == 3 and Dt.datetime.strptime(f"{com.text.split()[1]} {com.text.split()[2]}", '%d.%m.%Y %H:%M').timestamp() - time.time() > 59:
            if await self.is_cheker(com.reply_to_message.text, self.events_dict[com.chat.id].values()) == None:
                self.events_dict[com.chat.id].update({self.numb: [com.reply_to_message.text] + com.text.split()[1:]})
                asyncio.run(await self.event_timer(com.chat.id, self.events_dict[com.chat.id][self.numb], self.numb))
                self.numb += 1

        elif len(com.text.split()) == 2 and len(com.text.split()[1]) == 4 or len(com.text.split()[1]) == 5:
            if Dt.datetime.strptime(f"{Dt.datetime.now().date()} {com.text.split()[1]}", "%Y-%m-%d %H:%M").timestamp() - time.time() > 59:
                if await self.is_cheker(com.reply_to_message.text, self.events_dict[com.chat.id].values()) == None:
                    self.events_dict[com.chat.id].update({self.numb: [com.reply_to_message.text] + [com.text.split()[1]]})
                    asyncio.run(await self.event_timer(com.chat.id, self.events_dict[com.chat.id][self.numb], self.numb))
                    self.numb += 1

        elif len(com.text.split()) == 2 and len(com.text.split()[1]) == 10:
            if Dt.datetime.strptime(f"{com.text.split()[1]} 00:00", "%d.%m.%Y %H:%M").timestamp() - time.time() > 59:
                if await self.is_cheker(com.reply_to_message.text, self.events_dict[com.chat.id].values()) == None:
                    self.events_dict[com.chat.id].update({self.numb: [com.reply_to_message.text] + [com.text.split()[1]]})
                    asyncio.run(await self.event_timer(com.chat.id, self.events_dict[com.chat.id][self.numb], self.numb))
                    self.numb += 1

    async def events(self, chat_id):
        events = ""

        try:
            lol = self.events_dict[chat_id]
        except:
            self.events_dict.update({chat_id: dict()})
        for el, val in self.events_dict[chat_id].items():
            if len(val) == 3:
                events += f"●  {val[0]}\nДата: {val[1]}\nВремя: {val[2]}\n"
            elif len(val) == 2 and len(val[1]) == 10:
                events += f"●  {val[0]}\nДата: {val[1]}\n"
            elif len(val) == 2 and len(val[1]) == 5:
                events += f"●  {val[0]}\nВремя: {val[1]}\n"
        if events == "":
            await myBot.send_message(chat_id, "Cобытий нет(")
        else:
            await myBot.send_message(chat_id, f"События:\n{events}")