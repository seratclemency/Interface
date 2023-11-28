from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.boxlayout import MDBoxLayout
from googlesearch import search
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
        self.theme_cls.primary_palette = 'Red'
        screen = MDScreen()

        self.textinput = MDTextField(hint_text='Введите запрос',
                                pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                size_hint=(0.8, None),
                                on_text_validate=self.start_google_search)

        button1 = MDRaisedButton(text='Инструкция',
                                 pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                 size_hint=(0.8, None),
                                 on_press=self.show_instructions)
        self.intra = MDRaisedButton(text='Спарсить сервера Intra',
                                 pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                 size_hint=(0.8, None),
                                 on_press=self.start_parse_intra)

        dark_theme = MDSwitch(pos_hint={'center_x': 0.5, 'center_y': 0.1})
        dark_theme.bind(active=self.switch_theme)

        switch = MDSwitch(pos_hint={'center_x': 0.8, 'center_y': 0.9})
        switch.bind(active=self.switch)

        screen.add_widget(self.textinput)
        screen.add_widget(button1)
        screen.add_widget(switch)
        screen.add_widget(dark_theme)
        screen.add_widget(self.intra)
        return screen

    def show_instructions(self, instance):
        dialog = MDDialog(title='Инструкция',
                          text='Interface - это простое приложение, которое ищет рабочие сайты по вашему запросу. Вы вводите запрос на определённом языке (доступны английский и русский) и нажимаете на "Enter". Когда вы вводите запрос на русском языке вы должны оставить свич в правом верхнем углу в выключенном положении, а если на английском языке, то переключить свич в включённое положение. После этого у вас создастся файл по пути /storage/emulated/0 и в нём будут ссылки на рабочие сайты. Также есть функция для парсинга dns серверов для Intra. Для парсинга нажмите на соответствующую кнопку и по пути /storage/emulated/0 появится файл dns_servers.txt. Внизу находится свич темы приложения.')
        dialog.open()

    def start_google_search(self, instance):
        try:
            os.remove('/storage/emulated/0/working_links.txt')
            os.remove('/storage/emulated/0/not_working_links.txt')
        except Exception:
            pass
        self.show_start_dialog('Проверка началась. Это долго. Пожалуйста подождите около 5 минут и не выходите из приложения.')
        threading.Thread(target=self.google_search, args=(instance.text,)).start()

    def show_start_dialog(self, text):
        dialog = MDDialog(text=text)
        dialog.open()

    def show_start_intra_dialog(self, text):
        dialog = MDDialog(text=text)
        dialog.open()

    def start_parse_intra(self, instance):
        try:
            os.remove('/storage/emulated/0/dns_servers.txt')
        except Exception:
            pass
        self.show_start_intra_dialog('Парсинг закончился. Пожалуйста проверьте хранилище на наличие файла dns_servers.txt.')
        threading.Thread(target=self.parse_intra, args=(instance.text,)).start()

    def switch_theme(self, instance, value):
        if value:
            self.theme_cls.theme_style = 'Dark'
        else:
            self.theme_cls.theme_style = 'Light'

    def switch(self, instance, value):
        if value:
            self.language = 'RU'
        else:
            self.language = 'EN'

    def parse_intra(self, instance):
        try:
            url= 'https://github.com/curl/curl/wiki/DNS-over-HTTPS'
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', href=re.compile(r'dns-query$'))
            for link in links:
                full_url = link['href']
                with open('dns_servers.txt', 'a') as file:
                    file.write(full_url + '\n')
        except Exception:
            pass

    def google_search(self, query):
        if self.language == 'RU':
            ssl._create_default_https_context = ssl._create_unverified_context
            for i in search(query, tld='com', lang='ru', num=100, start=0, stop=None, pause=2.0):
                try:
                    req = requests.get(i, timeout=1)
                    if req.status_code == 200:
                        with open('working_links.txt', 'a') as file:
                            file.write(i + '\n')
                except Exception:
                    with open('not_working_links.txt', 'a') as file:
                        file.write(i + '\n')
        elif self.language == 'EN':
            ssl._create_default_https_context = ssl._create_unverified_context
            for i in search(query, tld='com', lang='en', num=100, start=0, stop=None, pause=2.0):
                try:
                    req = requests.get(i, timeout=1)
                    if req.status_code == 200:
                        with open('working_links.txt', 'a') as file:
                            file.write(i + '\n')
                except Exception:
                    with open('not_working_links.txt', 'a') as file:
                        file.write(i + '\n')

if __name__ == "__main__":
    MyKivyMDApp().run()