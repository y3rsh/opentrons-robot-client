import asyncio
import pprint

import aiohttp
import nest_asyncio  # pip install nest_asyncio
import opentrons.execute
import requests

nest_asyncio.apply()

headers = {"opentrons-version": "*"}


async def main():
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get("http://localhost:31950/health") as response:

            print("Status:", response.status)
            print("Content-type:", response.headers["content-type"])

            body = await response.text()
            pprint.pprint(body)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

########

protocol = opentrons.execute.get_protocol_api("2.12")
print(protocol.home())

#######
import requests  # pip install requests

headers = {"opentrons-version": "*"}
response = requests.get("http://localhost:31950/health", headers=headers)
print(response.text)
