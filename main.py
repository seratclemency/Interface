from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.storage.jsonstore import JsonStore
from googlesearch import search
import webbrowser
import requests
from bs4 import BeautifulSoup
import re
import ssl
import os
import threading


class MyKivyMDApp(MDApp):
    def __init__(self, **kwargs):
        super(MyKivyMDApp, self).__init__(**kwargs)
        self.language = 'RU'

    def build(self):
        self.theme_cls.primary_palette = 'Red' #Устанавливаем оттенок приложения на Красный
        screen = MDScreen() #Создаём объект screen который представляет собой окно приложения
        if not os.path.exists('/storage/emulated/0/Android/data/com.serat.onelove'):
            os.mkdir('/storage/emulated/0/Android/data/com.serat.onelove')
            if not os.path.exists('/storage/emulated/0/Android/data/com.serat.onelove/settings.json'):
                with open('/storage/emulated/0/Android/data/com.serat.onelove/settings.json', 'w') as file:
                    file.write('{"switch": {"state": false}, "theme": {"state": "Light"}, "language_switch": {"state": false}, "language": {"state": "EN"}}')
        else:
            pass

        self.store = JsonStore('/storage/emulated/0/Android/data/com.serat.onelove/settings.json')

        textinput = MDTextField(hint_text='Введите запрос',
                                pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                size_hint=(0.8, None),
                                on_text_validate=self.start_google_search) #Устанавливаем поле для ввода запроса

        instruction_button = MDRaisedButton(text='Инструкция',
                                 pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                 size_hint=(0.8, None),
                                 on_press=self.show_instructions) #Устанавливаем кнопку
        intra_button = MDRaisedButton(text='Спарсить сервера Intra',
                                 pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                 size_hint=(0.8, None),
                                 on_press=self.start_parse_intra) #Ещё кнопка
        github_button = MDIconButton(icon='github',
                                     pos_hint={'center_x': 0.9, 'center_y': 0.1},
                                     on_press=self.open_github_link)
        contacts_button = MDRaisedButton(text='Контакты',
                                         pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                         size_hint=(0.8, None),
                                         on_press=self.show_contacts)

        self.theme_cls.theme_style = self.store.get('theme')['state']
        self.language = self.store.get('language')['state']

        dark_theme = MDSwitch(pos_hint={'center_x': 0.5, 'center_y': 0.1}, active=self.store.get('switch')['state']) #Устанавливаем свич для переключения тёмной темы
        dark_theme.bind(active=self.switch_theme) #Привязываем свич к методу switch_theme

        switch = MDSwitch(pos_hint={'center_x': 0.8, 'center_y': 0.9}, active=self.store.get('language_switch')['state']) #Устанавливаем свич для переключения языка
        switch.bind(active=self.switch) #Привязываем свич к методу switch

        screen.add_widget(textinput) #Добавляем все кнопки в макет
        screen.add_widget(switch)
        screen.add_widget(dark_theme)
        screen.add_widget(intra_button)
        screen.add_widget(instruction_button)
        screen.add_widget(github_button)
        screen.add_widget(contacts_button)
        return screen #Возвращаем макет

    def show_instructions(self, instance): #Метод для показа диалогового окна Инструкций
        dialog = MDDialog(title='Инструкция',
                          text='Interface - это простое приложение, которое ищет рабочие сайты по вашему запросу. Вы вводите запрос на определённом языке (доступны английский и русский) и нажимаете на "Enter". Когда вы вводите запрос на русском языке вы должны оставить свич в правом верхнем углу в выключенном положении, а если на английском языке, то переключить свич в включённое положение. После этого у вас создастся файл по пути /storage/emulated/0 и в нём будут ссылки на рабочие сайты. Также есть функция для парсинга dns серверов для Intra. Для парсинга нажмите на соответствующую кнопку и по пути /storage/emulated/0 появится файл dns_servers.txt. Внизу находится свич темы приложения.') #Создаём окно
        dialog.open() #Открываем окно

    def show_contacts(self, instance):
        dialog = MDDialog(title='Контакты',
                          text='Made by serat in Turkmenistan.\nЕсли возникнут проблемы, то создайте issue на Github.\nЕсли хотите купить шавуху :)\nTelegram: @are_you_serat\nLink: @serat')
        dialog.open()

    def open_github_link(self, instance):
        webbrowser.open('https://github.com/SeratKlemence/Interface')

    def start_google_search(self, instance): #Метод для  начала проверки сайтов через новый поток
        try:
            os.remove('/storage/emulated/0/Android/data/com.serat.onelove/working_links.txt') #Удаление файлов с прошлой проверки если они есть
            os.remove('/storage/emulated/0/Android/data/com.serat.onelove/not_working_links.txt')
        except Exception:
            pass
        self.show_start_dialog('Проверка началась. Это долго. Пожалуйста подождите около 5 минут и не выходите из приложения.')
        threading.Thread(target=self.google_search, args=(instance.text,)).start() #Включение метода google_search в новом потоке дабы интерфейс приложения не зависал

    def show_start_dialog(self, text): #Ещё диалоговое окно
        dialog = MDDialog(text=text)
        dialog.open()

    def show_start_intra_dialog(self, text): #Ещё диалоговое окно
        dialog = MDDialog(text=text)
        dialog.open()

    def start_parse_intra(self, instance): #Метод для  начала парсинга серверов для Intra через новый поток
        try:
            os.remove('/storage/emulated/0/Android/data/com.serat.onelove/dns_servers.txt')
        except Exception:
            pass
        self.show_start_intra_dialog('Парсинг закончился. Пожалуйста проверьте хранилище на наличие файла dns_servers.txt.')
        threading.Thread(target=self.parse_intra, args=(instance.text,)).start() #Включение метода parse_intra в новом потоке дабы интерфейс приложения не зависал

    def switch_theme(self, instance, value): #Переключение темы. Если value = True, переключить темы на тёмную, иначе светлая
        if value:
            self.store.put('switch', state=True)
            self.store.put('theme', state='Dark')
            self.theme_cls.theme_style = 'Dark' #Тёмный фон
        else:
            self.store.put('switch', state=False)
            self.store.put('theme', state='Light')
            self.theme_cls.theme_style = 'Light' #Светлый фон

    def switch(self, instance, value): #Переключение языка. Если value = True, переключить язык на русский, иначе английский
        if value:
            self.store.put('language_switch', state=True)
            self.store.put('language', state='RU')
            self.language = 'RU'
        else:
            self.store.put('language_switch', state=False)
            self.store.put('language', state='EN')
            self.language = 'EN'

    def parse_intra(self, instance): #Метод для парсинга серверов
        try:
            url= 'https://github.com/curl/curl/wiki/DNS-over-HTTPS' #URL
            response = requests.get(url) #Отправка запроса
            html = response.text #Преобразование запроса в текст
            soup = BeautifulSoup(html, 'html.parser') #Создаём объект bs4
            links = soup.find_all('a', href=re.compile(r'dns-query$')) #Ищем только сервера в HTML коде которые имеют dns-query
            for link in links:
                full_url = link['href'] #Получаем ссылки
                with open('/storage/emulated/0/Android/data/com.serat.onelove/dns_servers.txt', 'a') as file: #Создаём файл
                    file.write(full_url + '\n') #Записываем в файл
        except Exception:
            pass

    def google_search(self, query): #Метод для проверки сайтов
        if self.language == 'RU': 
            ssl._create_default_https_context = ssl._create_unverified_context #Отключение проверки SSL сертификата чтоб не втыкал
            for i in search(query, tld='com', lang='ru', num=100, start=0, stop=None, pause=2.0): #Парсинг ссылок на сайты по запросам
                try:
                    req = requests.get(i, timeout=1) #Отправка get запроса с таймаутом в 1 секунду
                    if req.status_code == 200: #Если статус код запроса равен 200, то сайт рабочий
                        with open('/storage/emulated/0/Android/data/com.serat.onelove/working_links.txt', 'a') as file: #Создаём файл working_links.txt
                            file.write(i + '\n') #Записываем сайты в файл working_links.txt
                except Exception:
                    with open('/storage/emulated/0/Android/data/com.serat.onelove/not_working_links.txt', 'a') as file: #Иначе создаём файл not_working_links.txt
                        file.write(i + '\n') #Записываем не рабочие сайты в файл working_links.txt
        elif self.language == 'EN': #Всё тоже самое только для английского языка
            ssl._create_default_https_context = ssl._create_unverified_context
            for i in search(query, tld='com', lang='en', num=100, start=0, stop=None, pause=2.0):
                try:
                    req = requests.get(i, timeout=1)
                    if req.status_code == 200:
                        with open('/storage/emulated/0/Android/data/com.serat.onelove/working_links.txt', 'a') as file:
                            file.write(i + '\n')
                except Exception:
                    with open('/storage/emulated/0/Android/data/com.serat.onelove/not_working_links.txt', 'a') as file:
                        file.write(i + '\n')

if __name__ == "__main__":
    MyKivyMDApp().run()