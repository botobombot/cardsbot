# cardsbot
ээ саламалека 


короче. На линухе кали запускается так

sudo apt install python3-venv

python3 -m venv myenv

source myenv/bin/activate

дальше уже если винда, или если в окружении, то прописываем

pip install python-telegram-bot

дальше уже из папочки запускаем

python bot.py

все.
Токен если че на тестового бота так то на него пофиг.

файл с датабейз для создание дбшки и работы с ней. ну это просто
в файтсах непосредственно файтсы
в боте работа с ботом.

TODO:
1)Нормально сообщения не обрабатываются. Можно у бота настроить что он будет хавать условно "меню" и будет выдавать менюшку, а не прописывая /me. Надо бы понять короче как о может дефолтные соо обрабатывать

2)Привилегии. Можно в БДшке создать стат "Статус" у юзера. Он по нему и по айдишке в коде (двухфакторка) будет определять кто админ, кто там просто крутой и т.д. но не думаю что нужно выдавать роли кроме админской

3)подумать насчет био. Возможно убрать. Потому что любое взаимодействие с базой данных посредством текста - может оказаться фатальной. Вот что у меня щас написно - я могу, например, ломнуть БД и приписать себе админ права (если были бы). Для этого я и хочу создать двухфакторку + убрать текстовые поля, либо дать фозможность их править только админам.

4)раздать юзерам их карточки, сделать такой интерфейс короче.

5)интерфейс чтобы смотреть запросы - от кого и че. можно чтобы на сервер в логи записывал. Это оч просто сделать тоже.


Что щас бот делает в целом и так ясно, там есть на всякий менюшка. советую весь функционал кроме секретного заисывать туда.

сам бот @napisalhuynuBot
