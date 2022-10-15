from config import config
from typing import Union
from aio_utils import aio_get


async def bitcoin_price() -> Union[float, str]:
    try:
        data = await aio_get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
        btc = float(data["data"]["amount"])
    except:
        return "error with bitcoin price"
    return btc

async def ethereum_price() -> Union[float, str]:
    try:
        data = await aio_get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
        eth = float(data["data"]["amount"])
    except:
        return "error with ethereum price"
    return eth

async def beaconcha_status() -> str:
    # print('> beaconcha_status')VALIDATORS_INITIAL_BALANCE
    validators_indexes = config.VALIDATORS_INDEXES.split(",")
    validator_initial_balance = 32000000000 / 1000000000

    try:
        data = await aio_get('https://beaconcha.in/api/v1/validator/' + config.VALIDATORS_INDEXES)
        total_validators_balance = 0
        for v in data['data']:
            balance = v['balance'] / 1000000000 # maybe use bacance instead of effectivebalaca?
            total_validators_balance += balance
        total_initial_balance = validator_initial_balance * len(validators_indexes)
        total_profit = total_validators_balance - total_initial_balance
    except:
        return "error with beaconcha_status, block 1"

    try:
        data2 = await aio_get(f'https://beaconcha.in/api/v1/validator/{ config.VALIDATORS_INDEXES }/performance')
        total_daily_profit = 0.0
        for v in data2['data']:
            total_daily_profit += v['performance1d'] / 1000000000
        total_daily_profit = float(total_daily_profit)
    except:
        return "error with beaconcha_status, block 2"

#     reply = f'''BL / PROFIT: {total_validators_balance:.2f} / {total_profit:.2f} (${total_profit * self.eth_price:.0f})
# Daily: {total_daily_profit:.4f} (${total_daily_profit * self.eth_price:.0f})'''
    reply = f'''BL / PROFIT: {total_validators_balance:.2f} / {total_profit:.2f}'''
    return reply


async def fee_wallet_balance() -> str:
    api_key = config.ETHERSCAN_API_KEY
    fee_address = config.ETH_FEE_ADDRESS
    try:
        data = await aio_get(f'https://api.etherscan.io/api?module=account&action=balance&address={fee_address}&tag=latest&apikey={api_key}')
        balance = int(data['result']) / 10e17
    except:
        return "error with fee wallet balance"
    return balance