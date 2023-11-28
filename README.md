Interface - это простое приложение написанное на KivyMD, которое ищет рабочие сайты по вашему запросу. Оно будет полезно если вы находитесь в странах где массово блокируется интернет и где работающие сайты являются редкостью (Туркменистан, Иран и т.д).
Зависимости приложения: Kivy, KivyMD, requests, beautifulsoup4.
Для компилирования необходимо использовать buildozer. Советуется использовать Ubuntu 20.04 с Python версии 3.8.1 и выше или Google Colab.

Инструкция по компилированию:
Вся работа выполняется в Ubuntu 20.04
Установить buildozer. Инструкция: https://buildozer.readthedocs.io/en/latest/installation.html
Склонировать этот репозиторий: https://github.com/SeratKlemence/Interface.git
Можете отредактировать файл buildozer.spec по вашему усмотрению.
Перейти по директории к скронированному гиту, вызвать терминал и прописать команду buildozer android debug. Это скомпилирует дебаг версию приложения.
