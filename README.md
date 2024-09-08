# Mail Importer App

**Mail Importer App** — это веб-приложение для импорта и обработки писем из 
почтового ящика через IMAP с использованием WebSocket-соединения. Приложение 
может подключаться к почтовым серверам, загружать письма, фильтровать их и обрабатывать содержимое, включая вложения.

## Функционал

- Подключение к почтовым ящикам через IMAP
- Импорт и обработка писем
- Извлечение вложений и их обработка
- Логирование действий для мониторинга и отладки

## Требования

Для запуска приложения вам потребуется:

- **Python 3.8** или выше
- Активный почтовый ящик с поддержкой IMAP (например, _Gmail_, _Yandex_, 
  _Mail_)
- База данных **PostgreSQL**

## Старт проекта

Все зависимости перечислены в файле `requirements.txt` корня проекта.

Установите их командой:

```bash
pip install -r requirements.txt
```
Установите следующие переменные окружения для подключения к БД и ключ 
шифрования для безопасного хранения паролей клиентов:

```bash
export DB_NAME='your_database_name'
export DB_USER='your_database_user'
export DB_PASSWORD='your_database_password'
export PASSWORD_KEY='VQdUF9K_1DnuoMdKudLFVp5BQRp_9Ubt0pJ634GraXE='
```
#### Важно! 
> Значением **PASSWORD_KEY** должна быть строка Base64, которая представляет 
32 байта _(как в примере)_. 

Запустить проект с помощью **daphne** (при использовании WebSocket-соединения):
```bash
daphne -b 127.0.0.1 -p 8000 mail_importer.asgi:application
```
## Вклад
Если вы хотите внести вклад в проект, [создайте pull request](https://github.com/Gricana/mail_importer_app/pulls) или [откройте 
issue](https://github.com/Gricana/mail_importer_app/issues/new) на 
странице GitHub проекта.
