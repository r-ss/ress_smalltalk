import timeit
import asyncio
import pytest


from config import config

from crypt import bitcoin_price, ethereum_price, beaconcha_status, fee_wallet_balance
from weather import weather_bcn, weather_spb




@pytest.mark.asyncio
async def test_sleep():

    benchmark_start = timeit.default_timer()

    # for i in range(5):
    #     await api_imitate_display()
    # asyncio.run(main())

    # kettle = TaskWrapper(boil_kettle, timeout=2.0, errmsg="Err Kettle")
    # cups = TaskWrapper(clean_cups, 2.0, errmsg="Err Cups")
    # masha = TaskWrapper(fuck_masha, 2.0, errmsg="Err Masha")

    tasks = [bitcoin_price(), ethereum_price(), fee_wallet_balance(), beaconcha_status(), weather_spb(), weather_bcn()]
    btc_price, eth_price, fee_wallet, staking, weather_spbr, weather_bcnr = await asyncio.gather(*tasks)


    fee_wallet_usd = "err"
    if type(eth_price) == float:
        fee_wallet_usd = fee_wallet * eth_price

    m = f'''BTC: {btc_price:.0f}
ETH: {eth_price:.0f}
{ staking }
Fees: {fee_wallet:.4f} (${fee_wallet_usd:.1f})

{weather_spbr}
{weather_bcnr}'''


    # tm = TaskManager(tasks, timeout=1.5)
    # results = await tm.run()

    # results = await asyncio.gather(*tasks)
    print(m)


    

    # boiling_task = asyncio.create_task(boil_kettle(1.0), name="boiling kettle.")
    # clean_cups_task = asyncio.create_task(clean_cups(13), name="cleaning cups.")
    # done, pending = await asyncio.wait(
    #     [boiling_task, clean_cups_task],
    #     return_when=asyncio.ALL_COMPLETED  # asyncio.ALL_COMPLETED / FIRST_COMPLETED
    #     )
    # for task in pending:
    #     print(f"Task {task.get_name()} did not complete.")
    #     task.cancel()
    # for task in done:
    #     print(task.result())

    benchmark_end = timeit.default_timer() - benchmark_start

    

    
    print(f"Benchmark {benchmark_end:.2f} s")

    # results = await asyncio.gather(boil_kettle(1.2), clean_cups(2))
    # print(results)

    # try:
    #     result_k, result_c = await asyncio.wait_for(
    #         asyncio.gather(boil_kettle(1.2), clean_cups(2)),
    #         timeout=6.0,
    #     )

    #     print(result_k)
    #     print(result_c)

    # except asyncio.TimeoutError:
    #     print("oops took longer than 2s!")


