from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
from gevent import config

#tockens
payments_tocken = ''
tocken = ''


#apps
bot = Bot(token=tocken)
dp = Dispatcher(bot)

#prices
PRICE = types.LabeledPrice(label='Подписка на канал за 1 месяц!', amount=200*100) #в копейках

@dp.message_handler(commands=['buy'])
async def buy(message):

    #await bot.send_message(message.chat.id, 'Тестовый платеж!!!')
    await bot.send_invoice(
        message.chat.id,
        title='Подписка на бота',
        description='Активация подписки на бота на 1 месяц',
        provider_token=payments_tocken,
        currency='rub',
        photo_url='https://mobimg.b-cdn.net/v3/fetch/d0/d0a69ce499f28ff0a592875aeb4607ed.jpeg',
        photo_width=416,
        photo_height=234, 
        photo_size=416, 
        is_flexible=False, 
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload='test-invoice-payload'
    ) 


#pre checkout 10 sec
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout(pre_checkout_q):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

#successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message):
    print('УСПЕШНО!!!!')
    await bot.send_message(message.chat.id, 'Платеж успешно прошел!')


@dp.message_handler()
async def echo(message):
    await message.answer(message.text)


executor.start_polling(dp, skip_updates=False)