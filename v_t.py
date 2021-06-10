from  aiogram import Bot, types
import asyncio
from k_m import K_m

myBot = Bot(token="1779399322:AAG6TLSDv6pEECnFJdpgT77Msfqar9tSkQg")

descr = {'v_m' : 'мут', 'v_b' : 'бан', 'v_k' : 'кик', 'v_um' : 'анмут', 'v_ub' : 'разбан'}

class V_t:
    dict_v = dict()
    voters = dict()

    def __init__(self, *params):
        try:
            self.name = ''
            for el in params[1][1:]:
                self.name += ' ' + el
            self.user_id = params[0]
        except:
            pass

    async def vote_check(self, chat_id, typ):
        try:
            if len(self.dict_v[chat_id][typ]) != 0:
                for i in self.dict_v[chat_id][typ]:
                    if i in self.name:
                        return False
                return True
            else:
                return True
        except:
            return True

    async def wait(self, typ, mes):
        await asyncio.sleep(5)
        await myBot.delete_message(self.dict_v[mes.chat.id][typ][self.name][0].chat.id, self.dict_v[mes.chat.id][typ][self.name][0].message_id)

        if typ == 'v_m' and self.dict_v[mes.chat.id][typ][self.name][1]['+'] > self.dict_v[mes.chat.id][typ][self.name][1]['-']:
            await K_m(self.name.split()).mute(mes.chat.id)

        elif typ == 'v_b' and self.dict_v[mes.chat.id][typ][self.name][1]['+'] > self.dict_v[mes.chat.id][typ][self.name][1]['-']:
            await K_m(self.name.split()).ban(mes.chat.id)

        elif typ == 'v_k' and self.dict_v[mes.chat.id][typ][self.name][1]['+'] > self.dict_v[mes.chat.id][typ][self.name][1]['-']:
            await K_m(self.name.split()).kick(mes.chat.id)
            await K_m(self.name.split()).unban(mes.chat.id)

        elif typ == 'v_ub' and self.dict_v[mes.chat.id][typ][self.name][1]['+'] > self.dict_v[mes.chat.id][typ][self.name][1]['-']:
            await K_m(self.name.split()).unban(mes.chat.id)

        elif typ == 'v_um' and self.dict_v[mes.chat.id][typ][self.name][1]['+'] > self.dict_v[mes.chat.id][typ][self.name][1]['-']:
            await K_m(self.name.split()).unmute(mes.chat.id)

        del self.voters[mes.chat.id][self.dict_v[mes.chat.id][typ][self.name][0].message_id]
        del self.dict_v[mes.chat.id][typ][self.name]

    async def vote(self, mes, typ):
        b_1 = types.InlineKeyboardButton('+', callback_data=f'{typ}+')
        b_2 = types.InlineKeyboardButton('-', callback_data=f'{typ}-')
        v = types.InlineKeyboardMarkup().add(b_1, b_2)
        if not mes.chat.id in self.dict_v.keys():
            print('wtf')
            self.dict_v.update({mes.chat.id : {'v_m': dict(), 'v_b': dict(), 'v_k': dict(), 'v_um': dict(), 'v_ub': dict()}})

        self.dict_v[mes.chat.id][typ].update({self.name : [await myBot.send_message(mes.chat.id, f'Начато голосование: {descr[typ]}{self.name}', reply_markup=v), {'+' : 0, '-' : 0}]})