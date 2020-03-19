import random

import vk_api
import vk_bot
import Library

# --
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot import VkBot
# --

def write_atmt(user_id, attachment):
    vk.method('messages.send', {'user_id': user_id, 'attachment': attachment, 'random_id': random.randint(0, 1737)})

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 1737)})

def send_photo_Anel(photo_id):
    vk.method('messages.send', {'user_id': 243811811, 'attachment': photo_id, 'random_id': random.randint(0, 1737)})



# API-ключ созданный ранее
token = vk_bot.token

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            bot = VkBot(event.user_id)

            type = event.attachments.get("attach1_type")

            if event.text == "Картиночка":
                write_atmt(event.user_id, bot.new_message(event.text))

            elif event.text == "Музычка":
                write_atmt(event.user_id, bot.new_message(event.text))

            elif event.text == "Видосик":
                write_atmt(event.user_id, bot.new_message(event.text))

            elif event.text == "♂♂♂":
                write_atmt(event.user_id, bot.new_message("Gachi"))

            elif event.text != "":
                if bot.new_message(event.text):
                    if bot.new_message(event.text) == "None":
                        stk = Library.Sticker[random.randint(0, len(Library.Sticker) - 1)]
                        write_atmt(event.user_id, stk)
                    else:
                        write_msg(event.user_id, bot.new_message(event.text))

            else:
                stk = Library.Sticker[random.randint(0, len(Library.Sticker)-1)]
                write_atmt(event.user_id, stk)