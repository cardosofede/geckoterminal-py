import asyncio
from typing import Optional

import aiohttp

class GeckoTerminalClient:
    base_url = "https://api.geckoterminal.com/api/v2"
    headers = {
        "Accept": "application/json;version=20230302",
    }

    def __init__(self):
        self.ev_loop = self.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.ev_loop, headers=self.headers)

    @staticmethod
    def get_event_loop():
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            ev_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(ev_loop)
            return ev_loop

    async def api_request(self, method: str, path: str, params: Optional[dict] = None):
        async with self.session.request(method, f"{self.base_url}/{path}", params=params) as resp:
            if resp.status != 200:
                raise Exception(f"Error getting {path}: {resp.status}")
            return await resp.json()

    async def get_networks(self):
        return await self.api_request("GET", "networks")

    def get_networks_sync(self):
        return self.ev_loop.run_until_complete(self.get_networks())

    async def get_dexes_by_network(self, network_id: str):
        return await self.api_request("GET", f"networks/{network_id}/dexes")

    def get_dexes_by_network_sync(self, network_id: str):
        return self.ev_loop.run_until_complete(self.get_dexes_by_network(network_id))

    async def get_top_pools_by_network(self, network_id: str):
        return await self.api_request("GET", f"networks/{network_id}/pools")

    def get_top_pools_by_network_sync(self, network_id: str):
        return self.ev_loop.run_until_complete(self.get_top_pools_by_network(network_id))



if __name__ == "__main__":
    client = GeckoTerminalClient()
    # loop = asyncio.get_event_loop()
    # networks_async = loop.run_until_complete(client.get_networks())
    networks_sync = client.get_networks_sync()
    dexes = client.get_dexes_by_network_sync(networks_sync["data"][0]["id"])
    print(networks_sync)


