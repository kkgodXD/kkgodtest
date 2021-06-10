from pymongo import *
from aiogram import Bot, types, Dispatcher, executor
from pi_ev import Pin_ev
from k_m import K_m
from v_t import V_t
import datetime

dict_votes = {'/votemute' : 'v_m', '/voteban' : 'v_b', '/votekick' : 'v_k', '/voteunmute' : 'v_um', '/voteunban' : 'v_ub'}

perm_dict = {'admin' : {'kick' : 1, 'mute' : 1, 'changeperm' : 2, 'showperm' : 1, 'ban' : 1, 'pinup' : 1, 'event' : 1, 'write_mes' : 1},
             'user' : {'kick' : 0, 'mute' : 0, 'changeperm' : 0, 'showperm' : 0, 'ban' : 0, 'pinup' : 0, 'event' : 0, 'write_mes' : 1},
             'moderator': {'kick' : 1, 'mute' : 1, 'changeperm' : 1, 'showperm' : 1, 'ban' : 0, 'pinup' : 1, 'event' : 1, 'write_mes' : 1},
             'creator' : {'kick' : 1, 'mute' : 1, 'changeperm' : 3, 'showperm' : 1, 'ban' : 1, 'pinup' : 1, 'event' : 1, 'write_mes' : 1},
             'looking' : {'write_mes' : 0}
             }

client = MongoClient('localhost', 27017)
db_obj = client['users_bot_mn']

myBot = Bot(token="1779399322:AAG6TLSDv6pEECnFJdpgT77Msfqar9tSkQg")
dp = Dispatcher(myBot)

inv_keyb = types.InlineKeyboardMarkup()
button_1 = types.InlineKeyboardButton("Комманды бота📲", url='https://telegra.ph/Kommandy-bota-03-25')
button_2 = types.InlineKeyboardButton("Функционал📘", url='https://telegra.ph/Funkcional-03-26')
button_3 = types.InlineKeyboardButton("Помощь✉️", callback_data='two')
button_4 = types.InlineKeyboardButton("Правила📗", url='https://telegra.ph/Pravila-03-26-10')
button_5 = types.InlineKeyboardButton("Начать работу с ботом!🗼", callback_data='four')
inv_keyb.add(button_1, button_2)
inv_keyb.add(button_3, button_4)
inv_keyb.add(button_5)

async def reg(com):
    user = com.from_user
    try:
        chat_id = com.chat.id
    except:
        chat_id = com.message.chat.id

    if not user.id in [el['user_id'] for el in list(db_obj[str(chat_id)].find({}, {'user_id' : 1}))]:
        if user.id not in [el.user.id for el in list(await myBot.get_chat_administrators(chat_id))]:
            db_obj[str(chat_id)].insert_one({'user_id': user.id, 'reg' : datetime.datetime.now(), 'nickname': user.username, 'full_name' : user.full_name, 'role': 'user'})

        else:
            if [el.is_chat_creator() for el in list(await myBot.get_chat_administrators(chat_id)) if el.user.id == user.id][0]:
                db_obj[str(chat_id)].insert_one({'user_id': user.id, 'reg' : datetime.datetime.now(), 'nickname': user.username, 'full_name' : user.full_name, 'role': 'creator'})
            else:
                db_obj[str(chat_id)].insert_one({'user_id': user.id, 'reg' : datetime.datetime.now(), 'nickname': user.username, 'full_name' : user.full_name, 'role': 'admin'})

@dp.message_handler(commands=['start', 'ban', 'unban', 'voteban', 'voteunban', 'kick', 'votekick', 'roles', 'role',
                              'pinup', 'denup', 'pinups', 'events', 'event', 'mute', 'votemute', 'unmute', 'changeperm',
                              'voteunmute', 'audit', 'showperm', 'get_name'])
async def commands(com: types.Message):
    if com.chat.type != 'private' and com.from_user.is_bot == False:
        await reg(com)

    user_role = tuple(db_obj[str(com.chat.id)].find({'user_id' : com.from_user.id}, {'role' : 1}))[0]['role']
    if com.text == '/start' and com.chat.type == 'private':
        await myBot.send_message(com.chat.id, "Привет, я бот-управляющий для групп! Я многое могу так что советую прочитать про мой функционал!"
                                        "(Тап по кнопке). Так же, как и всех уважающих себя ботов - у меня есть правила. По этому чтобы пользоваться моими функциями правильно"
                                        ", прочитай их! Для начала работы, тап по кнопке!", reply_markup=inv_keyb)

    elif com.text == '/get_name' and com.reply_to_message != None:
        if not com.reply_to_message.from_user.username == None:
            await myBot.send_message(com.chat.id, f"Полное имя - [{com.reply_to_message.from_user.full_name}] | Никнейм - [{com.reply_to_message.from_user.username}]")
        else:
            await myBot.send_message(com.chat.id, f'Полное имя - [{com.reply_to_message.from_user.full_name}]')
        await reg(com.reply_to_message)

    elif com.text == '/pinup' and com.reply_to_message != None and perm_dict[user_role]['pinup'] == 1:
       await Pin_ev().pinup(com)

    elif com.text.split()[0] == '/denup' and perm_dict[user_role]['pinup'] == 1:
       await Pin_ev().denup(com)

    elif com.text == '/pinups':
       await Pin_ev().pinups(com)

    elif com.text.split()[0] == '/event' and len(com.text.split()) > 1 and com.reply_to_message != None and perm_dict[user_role]['event'] == 1:
        try:
            await Pin_ev().event(com)
        except:
            pass

    elif com.text == '/events':
       await Pin_ev().events(com.chat.id)

    elif com.text.split()[0] == '/mute' and len(com.text.split()) > 1 and perm_dict[user_role]['mute'] == 1:
        try:
            await K_m(com.text.split()[1:], com.chat.id).mute(com.chat.id, com.text)
        except:
            pass


    elif com.text.split()[0] == '/unmute' and len(com.text.split()) > 1 and perm_dict[user_role]['mute'] == 1:
        try:
            if tuple(db_obj[str(com.chat.id)].find({'user_id' : K_m(com.text.split()[1:], com.chat.id).user_id}, {'role': 1}))[0]['role'] != 'looking':
                await K_m(com.text.split()[1:], com.chat.id).unmute(com.chat.id)
        except:
            pass

    elif com.text.split()[0] == '/support':
        try:
            await myBot.send_message(com.chat.id, f'Наш официальный саппорт-бот - @support_jackson')
        except:
            pass

    elif '/vote' in com.text.split()[0] and len(com.text.split()) > 1 and await V_t(K_m(com.text.split()[1:], com.chat.id).user_id, com.text.split()[1:]).vote_check(com.chat.id, 'v_m'):
        try:
            role = tuple(db_obj[str(com.chat.id)].find({'user_id' : K_m(com.text.split()[1:], com.chat.id).user_id}, {'role': 1}))[0]['role']
            typ = dict_votes[com.text.split()[0]]
            if role == 'user':
                    await V_t(K_m(com.text.split()[1:], com.chat.id).user_id, com.text.split()).vote(com, typ)
                    await V_t(K_m(com.text.split()[1:], com.chat.id).user_id, com.text.split()).wait(typ, com)

            elif user_role != 'user' and role == 'moderator':

                await V_t(K_m(com.text.split()[1:], com.chat.id).user_id, com.text.split()).vote(com, typ)
                await V_t(K_m(com.text.split()[1:], com.chat.id).user_id, com.text.split()).wait(typ, com)

        except:
            pass


    elif com.text.split()[0] == '/changeperm' and len(com.text.split()) > 2 and perm_dict[user_role]['changeperm'] != 0:
        await K_m(com.text.split()[1:-1], com.chat.id).changeperm(com, perm_dict[user_role]['changeperm'])

    elif com.text == '/showperm':
        await myBot.send_message(com.chat.id, user_role, reply_to_message_id = com.message_id)

    elif com.text.split()[0] == '/kick' and len(com.text.split()) > 1 and perm_dict[user_role]['kick'] == 1:
        try:
            await K_m(com.text.split()[1:], com.chat.id).kick(com.chat.id)
            await K_m(com.text.split()[1:], com.chat.id).unban(com.chat.id)
        except:
            pass

    elif com.text.split()[0] == '/ban' and len(com.text.split()) > 1 and perm_dict[user_role]['ban'] == 1:
        try:
            await K_m(com.text.split()[1:], com.chat.id).ban(com.chat.id, com.text)
        except:
            pass

    elif com.text.split()[0] == '/unban' and len(com.text.split()) > 1 and perm_dict[user_role]['ban'] == 1:
        try:
            await K_m(com.text.split()[1:], com.chat.id).unban(com.chat.id)
        except:
            pass

    elif com.text.split()[0] == '/checkrules':
        await myBot.send_message(com.chat.id, f'Правила данной беседы:\n {s}')

    elif com.text.split()[0] == '/roles':
        await myBot.send_message(com.chat.id, f'Список ролей:\nAdmin <3\nUser <3\nCreator <3\nModerator <3\nLooking <3')

#    elif com.text.split()[0] == '/showinfo' and com.reply_to_message != None:
#        if db_obj[com.chat.id].find({'user_id': com.from_user.id}, {'role': 1}) == True:
#            tuple(db_obj[com.chat.id].find({'user_id': com.from_user.id}, {'role': 1}))[0]['role'] == 'admin':
#            myBot.send_message(com.chat.id, db_obj[com.chat.id].find({com.text.split()[1] :  }) )
    elif com.text.split()[0] == '/clearchat' and db_obj[com.chat.id].find({'user_id': com.from_user.id}, {'role': 1}):
        myBot.delete_message(com.chat.id, com.message_id)


@dp.message_handler(content_types= ['text'])
async def mблessages(mes: types.Message):
    if mes.chat.type != 'private' and mes.from_user.is_bot == False:
        await reg(mes)

@dp.message_handler(content_types= ['new_chat_members'])
async def messages(mes: types.Message):
    if mes.from_user.is_bot == False:
        await reg(mes)

@dp.message_handler(content_types=['left_chat_member'])
async def messages(mes: types.Message):
    pass

@dp.callback_query_handler(lambda call: True)
async def main_menu_quaries(call):
    if call.message.chat.type != 'private':
        await reg(call)

    if call.data == 'two':
        await myBot.send_message(call.message.chat.id, "Наши контакты:\n@sashokchik\n@krempyc")

    elif call.data == 'four':
        await myBot.send_message(call.message.chat.id, "das")

    elif 'v_' in call.data:
        try:
            vot = V_t().voters[call.message.chat.id][call.message.message_id]
        except:
            vot = list()

        if not call.from_user.id in vot:
            if len(V_t().voters) != 0:
                V_t().voters[call.message.chat.id][call.message.message_id].append(call.from_user.id)
            else:
                V_t().voters.update({call.message.chat.id: {call.message.message_id: [call.from_user.id]}})

            if '+' in call.data:
                V_t().dict_v[call.message.chat.id][call.data[:-1]][' ' + ' '.join(call.message.text.split()[3:])][1]['+'] += 1
            else:
                V_t().dict_v[call.message.chat.id][call.data[:-1]][' ' + ' '.join(call.message.text.split()[3:])][1]['-'] += 1

        if sum(list(V_t().dict_v[call.message.chat.id][call.data[:-1]][' ' + ' '.join(call.message.text.split()[3:])][1].values())) == len(tuple(db_obj[str(call.message.chat.id)].find({}))):
            await myBot.delete_message(call.message.chat.id, call.message.message_id)

            del V_t().voters[call.message.chat.id][call.message.message_id]
            problem = V_t().dict_v[call.message.chat.id][call.data[:-1]][' ' + ' '.join(call.message.text.split()[3:])][1]
            prov = problem['+'] > problem['-']
            del V_t().dict_v[call.message.chat.id][call.data[:-1]][' ' + ' '.join(call.message.text.split()[3:])]

            if 'v_m' in call.data and prov:
                await K_m(call.message.text.split()[3:], call.message.chat.id).mute(call.message.chat.id)
            elif 'v_um' in call.data and prov:
                await K_m(call.message.text.split()[3:], call.message.chat.id).unmute(call.message.chat.id)
            elif 'v_k' in call.data and prov:
                await K_m(call.message.text.split()[3:], call.message.chat.id).kick(call.message.chat.id)
                await K_m(call.message.text.split()[3:], call.message.chat.id).unban(call.message.chat.id)
            elif 'v_b' in call.data and prov:
                await K_m(call.message.text.split()[3:], call.message.chat.id).ban(call.message.chat.id)
            elif 'v_ub' in call.data and prov:
                await K_m(call.message.text.split()[3:], call.message.chat.id).unban(call.message.chat.id)

executor.start_polling(dp, skip_updates=True)