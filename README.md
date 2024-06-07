![Python 3.12.3](https://img.shields.io/badge/Python-3.12.3-blue)

# Телеграм бот "Угадай число!"
Телеграм бот написан на python 3.12.3, использует telegram webhook.

Для запуска телеграм бота через Container Apps понадобится:
- Создать телеграм бота через BotFather - получить токен
- Собрать docker образ и запушить его в Artifact Registry
- Создать Container App
- Добавить webhook в telegram  


## Создание Container App
При создании Container App необходимо:
1. Указать название
2. Включить создание публичного адреса (используется для webhook)
3. Выбрать docker образ с телеграм ботом
4. `Порт контейнера` указать: 8080
5. В разделе `Переменные` добавить: BOT_TOKEN=`токен_из_bot_father` 
6. Конфигурацию можно поставить `мин кол-во экземпляров` в 0

### Добавление webhook в telegram 
Для работы telegram bot необходимо добавить webhook.
Заменить:
- `{BOT_TOKEN}` - поставить токен телеграм бота
- `{PUBLIC_URL}` - поставить публичный адрес

Шаги:
1. Проверить существуют ли webhook: `https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo`
2. Если есть webhook, то удалить: `https://api.telegram.org/bot{BOT_TOKEN}/setWebhook`
3. Добавить новый webhook: `https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={PUBLIC_URL}/{BOT_TOKEN}`
