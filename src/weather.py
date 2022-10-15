from aio_utils import aio_get

async def weather_spb() -> str:
    try:
        r = await aio_get('http://wttr.in/Saint%20Petersburg?m&format=3', as_text=True)
    except:
        return "error with Saint-Petersburg weather"
    return r.strip()

async def weather_bcn() -> str:
    try:
        r = await aio_get('http://wttr.in/Barcelona?m&format=3', as_text=True)
    except:
        return "error with Barcelona weather"
    return r.strip()