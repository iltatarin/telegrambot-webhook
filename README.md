![Python 3.12.3](https://img.shields.io/badge/Python-3.12.3-blue)

# Телеграм бот "Угадай число!"
Телеграм бот написан на python 3.12.3 с использование aiogram и aiohttp, telegram webhook.

Для запуска телеграм бота через Container Apps необходимо:
- Получить токен для телеграм бота - написать @BotFather
- Собрать и запушать docker образ в Artifact Registry
- Создать Container Apps
- Добавить webhook в telegram  


## Создание Container App
При создании Container App необходимо:
1. Включить создание публичного адреса (будет использоваться для webhook)
2. Выбрать docker образ с телеграм ботом
3. В разделе `Переменные` добавить: BOT_TOKEN=`токен_из_bot_father` 
4. В разделе `Конфигурация` выбрать 0.5 vCPU (если выбрать меньше, то cold start станет больше) 
5. `Мин кол-во экземпляров` поставить в 0 (cold start)

### Добавление webhook в telegram 
Чтобы bot мог получать сообщения из telegram, небходимо добавить webhook:
- Вместо `{BOT_TOKEN}` - поставить токен телеграм бота
- Вместо `{PUBLIC_URL}` - поставить публичный адрес

Шаги:
1. Проверить существуют ли webhook: `https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo`
2. Удалить существующие webhook: `https://api.telegram.org/bot{BOT_TOKEN}/setWebhook`
3. Добавить новый webhook: `https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={PUBLIC_URL}/{BOT_TOKEN}`
