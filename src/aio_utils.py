import asyncio
import aiohttp

async def aio_get(url: str, timeout=5.0, as_text=False):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=timeout) as resp:
                if as_text:
                    result = await resp.text()
                else:
                    result = await resp.json()
        except asyncio.exceptions.TimeoutError:
            raise Exception("timeout")
    return result