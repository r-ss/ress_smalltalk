from datetime import datetime, time
import logging
# from emoji import emojize
import asyncio

from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackContext
# from telegram.ext import Application
# import mongoengine as mongoengine

from config import config

from telegram_commands import TelegramCommand, TelegramCommandsBin

from crypt import bitcoin_price, ethereum_price, beaconcha_status, fee_wallet_balance
from weather import weather_bcn, weather_spb
from analytics import get_websites_analytics


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

application = Application.builder().token(config.BOT_TOKEN).build()

async def send(message: str) -> None:
    await application.bot.send_message(chat_id=config.CHAT_ID, text=message)

async def info_crypto(update: Update, context: CallbackContext = None):
    tasks = [bitcoin_price(), ethereum_price(), fee_wallet_balance(), beaconcha_status()]
    btc_price, eth_price, fee_wallet, staking = await asyncio.gather(*tasks)

    fee_wallet_usd = "err"
    if type(fee_wallet) == float and type(eth_price) == float:
        fee_wallet_usd = fee_wallet * eth_price
        fee_wallet_usd = f"${fee_wallet_usd:.1f}"
        fee_wallet = f"{fee_wallet:.4f}"

    m = f'''BTC: {btc_price:.0f}
ETH: {eth_price:.0f}
{ staking }
Fees: {fee_wallet} ({fee_wallet_usd})
'''
    if update:
        await update.message.reply_text(m)
        return ConversationHandler.END
    await send(m)


async def info_weather(update: Update, context: CallbackContext = None):
    w_spb, w_bcn = await asyncio.gather(weather_spb(), weather_bcn())
    m = f"{w_spb}\n{w_bcn}"
    if update:
        await update.message.reply_text(m)
        return ConversationHandler.END
    await send(m)

async def info_websites_analytics(update: Update, context: CallbackContext = None):
    m = get_websites_analytics()
    if update:
        await update.message.reply_text(m)
        return ConversationHandler.END
    await send(m)

async def morning_routine(context: CallbackContext):
    await info_crypto(update=None)
    await info_weather(update=None)
    # await application.bot.send_message(chat_id=config.CHAT_ID, text="Kukusiki Send /start")

async def wrapper_all(update: Update, context: CallbackContext):

    await info_crypto(update=None)
    await info_weather(update=None)
    await info_websites_analytics(update=None)
    # await application.bot.send_message(chat_id=config.CHAT_ID, text="Kukusiki Send /start")



async def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text('Bye!')
    return ConversationHandler.END



commands = TelegramCommandsBin()

commands.add(TelegramCommand("crypto", info_crypto, description="show crypto stats"))
commands.add(TelegramCommand("weather", info_weather, description="show current weather"))
commands.add(TelegramCommand("web", info_websites_analytics, description="show web stats"))
commands.add(TelegramCommand("all", wrapper_all, description="show all"))



async def show_commands_list(update: Update, context: CallbackContext) -> None:
    await commands.show_commands_list(update, context)




async def bio(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    # logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("kkk")

    return ConversationHandler.END


def newapp() -> None:
    

    # Command handlers
    commands.setup_handlers(application)
    application.add_handler(CommandHandler("help", show_commands_list))

    # updater.start_webhook(listen='0.0.0.0',
    #                       port=config.PORT, url_path=config.BOT_TOKEN,
    #                       webhook_url='https://existence-bot.ress.ws/' + config.BOT_TOKEN)

    # print("pizda")

    jobtime = time(hour = 8, minute = 0, second = 5, tzinfo=config.TZ)
    application.job_queue.run_daily(morning_routine, time=jobtime, name='morning-routine')

    # on different commands - answer in Telegram
    # application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("bio", bio))

    # on non command i.e message - echo the message on Telegram
    # application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    # main()
    newapp()
