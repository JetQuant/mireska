import bs4 as bs4
import requests
import random
import vk_api
import Library
import os

from io import BytesIO
from vk_api.upload import VkUpload

token = os.environ.get('BOT_TOKEN')  # access_token
vk = vk_api.VkApi(token=token)
vk_m = vk.get_api()
upload = VkUpload(vk_m)


class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = [
            ["ДАЛЕЕ", "НАЗАД", "НЕ РАБОТАЕТ"],      # 0
            ['ФАКТ'],                               # 1
            ["КАРТИНОЧКА"],                         # 2
            ["ВИДОСИК"],                            # 3
            ["МУДРОСТЬ"],                           # 4
            ["АНЕКДОТИК"],                          # 5
            ["ЪУЪ"],                                # 6
            ["МУЗЫЧКА"]                             # 7
        ]

        self._ANSWER = [
            ['ПрИвЕт', 'Приветикиии', "Привет-привет", "Здравия желаю"],  # 0 Privet
            ["Сижу вооотб, учууусь((("],  # 1 Kak dela?
            ["Пока-пока", "До встречи", "Пока", "Покаааааа", "Покиии"],  # 2 Poka
            ["Sas"],  # 3
            ["Rofl"],  # 4
            ["Mireska"]  # 5
        ]

    def _get_user_name_from_vk_id(self, user_id):

        request = requests.get("https://vk.com/id" + str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_photo(self, photo_id):
        photo_src = f"photo{photo_id}"
        return photo_src

    def new_message(self, message):

        theme = -1

        for i in range(len(self._COMMANDS)):
            for j in range(len(self._COMMANDS[i])):
                if message.upper() == self._COMMANDS[i][j]:
                    theme = i
        # Привет
        if theme == 0:
            return "Хорошо"

        # ФАКТ
        elif theme == 1:
            return f"{self._get_fact()}"

        # # Картиночка
        # elif theme == 2:
        #     id_photo = 457239137 + random.randint(0, 243)
        #     return vk_m.messages.send(
        #         peer_id=self._USER_ID,
        #         attachment=f"photo423681797_{id_photo}",
        #         random_id=0)

        # Картиночка
        elif theme == 2:
            return self.send_photo(upload, self._get_photo())

        # Видосик
        elif theme == 3:
            video_id = f"video{Library.Video[random.randint(0, len(Library.Video)-1)]}"
            return video_id

        # МУДРОСТЬ
        elif theme == 4:
            return f"{self._get_wisdom()}"

        # Анекдотик
        elif theme == 5:
            return f"ВНИМАНИЕ!!! АНЕКДОТ: \n {self._get_joke()}"

        # ЪуЪ
        elif theme == 6:
            return "ЬеЬ"

        # Музычка
        elif theme == 7:
            music_id = f"audio{Library.Audio[random.randint(0, len(Library.Audio)-1)]}"
            return music_id

        else:
            return f"None"

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    def _get_photo(self):

        err = 404

        while err == 404:
            page = requests.get(f'https://avavatar.ru/image/{random.randint(1, 40895)}')
            soup = bs4.BeautifulSoup(page.text, "html.parser")

            if soup.findAll('div', class_="code"):
                continue

            else:
                img = soup.findAll('img', class_="image_original")
                err = 0

        photo = f"https://avavatar.ru{self._get_src(str(list(img)[0]))}.jpg"

        return photo

    def _get_wisdom(self):

        page = requests.get('https://randstuff.ru/saying/')
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        wisdom = soup.findAll('td')

        return self._clean_all_tag_from_str(str(list(wisdom)[0]))

    def _get_fact(self):

        page = requests.get('https://randstuff.ru/fact/')
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        fact = soup.findAll('td')

        return self._clean_all_tag_from_str(str(list(fact)[0]))

    def _get_joke(self):

        page = requests.get('https://nekdo.ru/random/')
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        anekdot = soup.findAll('div', class_='text')

        return self._clean_all_tag_from_str(str(list(anekdot)[0]))

    def _get_sticker(self):

        page = requests.get(f'http://vkclub.su/ru/stickers/?sortby=date&orderby=desc&page={random.randint(0, 16)}')
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        mainSTK = soup.findAll('a', class_="catlink rc_link")

        nameSticker = self.get_href(str(mainSTK[random.randint(0, len(mainSTK) - 1)]))

        page = requests.get(f'http://vkclub.su/ru/stickers/{nameSticker}/')
        soup = bs4.BeautifulSoup(page.text, "html.parser")
        numberSticker = soup.findAll('a', class_="stickerlistitem")

        rnd = random.randint(0, len(numberSticker) - 1)

        if rnd < 10:
            Sticker = f"http://vkclub.su/_data/stickers/{nameSticker}/sticker_vk_{nameSticker}_00{rnd}.png"
        else:
            Sticker = f"http://vkclub.su/_data/stickers/{nameSticker}/sticker_vk_{nameSticker}_0{rnd}.png"

        return Sticker

    @staticmethod
    def get_href(string_line):

        result = ""
        flag = 0

        for i in list(string_line):

            if i == "/":
                flag += 1

            elif flag == 3:
                result += i

        return result

    @staticmethod
    def _get_src(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = False
        src = ""
        flag = 0
        flagSRC = 0

        for i in list(string_line):

            if i == ".":
                not_skip = False
                flagSRC = 3

            elif not_skip and flagSRC != 3:
                result += i

            elif flag == 4:
                not_skip = True

            elif flag == 0 and i == "s":
                src += i
                flag = 1

            elif flag == 1 and i == "r":
                src += i
                flag = 2
            elif flag == 1 and i != "r":
                src = ""
                flag = 0

            elif flag == 2 and i == "c":
                src += i
                flag = 3
            elif flag == 2 and i != "c":
                src = ""
                flag = 0

            elif flag == 3 and i == "=":
                src += i
                flag = 4

        return result

    def send_photo(self, upload, url):

        img = requests.get(url).content
        f = BytesIO(img)

        response = upload.photo_messages(f)[0]

        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']

        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

        return attachment

    def send_dock(self, upload, url):

        img = requests.get(url).content
        f = BytesIO(img)

        response = upload.document_message(f)[0]

        owner_id = response['owner_id']
        photo_id = response['id']
        access_key = response['access_key']

        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

        return attachment

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True
        return result
