import asyncio
from typing import Optional
from glom import glom
import pandas as pd

import aiohttp

import geckoterminal_py.constants as CONSTANTS


class GeckoTerminalClient:
    base_url = "https://api.geckoterminal.com/api/v2"
    headers = {
        "Accept": "application/json;version=20230302",
    }

    def __init__(self):
        self.ev_loop = self.get_event_loop()
        self.session = aiohttp.ClientSession(loop=self.ev_loop, headers=self.headers)

    def close(self):
        self.ev_loop.run_until_complete(self.session.close())

    @staticmethod
    def get_event_loop():
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            ev_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(ev_loop)
            return ev_loop

    async def api_request(self, method: str, path: str, params: Optional[dict] = None) -> dict:
        # TODO: Review pagination and rate limits
        async with self.session.request(method, f"{self.base_url}/{path}", params=params) as resp:
            if resp.status != 200:
                raise Exception(f"Error getting {path}: {resp.status}")
            return await resp.json()

    async def get_networks(self) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_NETWORKS_PATH)
        spec = ('data', [{'id': 'id', 'type': 'type', 'name': ('attributes.name',),
                          'coingecko_asset_platform_id': ('attributes.coingecko_asset_platform_id',)}])
        networks = glom(response, spec)
        return pd.DataFrame(networks)

    def get_networks_sync(self) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_networks())

    # TODO: Implement get pool by network and pool id

    async def get_dexes_by_network(self, network_id: str) -> pd.DataFrame:
        # TODO: Request more stats about the dexes
        response = await self.api_request("GET", CONSTANTS.GET_DEXES_BY_NETWORK_PATH.format(network_id))
        spec = ('data', [{'id': 'id', 'type': 'type', 'name': ('attributes.name',)}])
        dexes_by_network = glom(response, spec)
        return pd.DataFrame(dexes_by_network)

    def get_dexes_by_network_sync(self, network_id: str) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_dexes_by_network(network_id))

    async def get_top_pools_by_network(self, network_id: str) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_TOP_POOLS_BY_NETWORK_PATH.format(network_id))
        spec = ('data', [{'id': 'id', 'type': 'type',
                          'name': ('attributes.name',),
                          "base_token_price_usd": ("attributes.base_token_price_usd",),
                          "base_token_price_native_currency": ("attributes.base_token_price_native_currency",),
                          "quote_token_price_usd": ("attributes.quote_token_price_usd",),
                          "quote_token_price_native_currency": ("attributes.quote_token_price_native_currency",),
                          "address": ("attributes.address",),
                          "reserve_in_usd": ("attributes.reserve_in_usd",),
                          "pool_created_at": ("attributes.pool_created_at",),
                          "fdv_usd": ("attributes.fdv_usd",),
                          "market_cap_usd": ("attributes.market_cap_usd",),
                          "price_change_percentage_h1": ("attributes.price_change_percentage.h1",),
                          "price_change_percentage_h24": ("attributes.price_change_percentage.h24",),
                          "transactions_h1_buys": ("attributes.transactions.h1.buys",),
                          "transactions_h1_sells": ("attributes.transactions.h1.sells",),
                          "transactions_h24_buys": ("attributes.transactions.h24.buys",),
                          "transactions_h24_sells": ("attributes.transactions.h24.sells",),
                          "volume_usd_h24": ("attributes.volume_usd.h24",),
                          'dex_id': ('relationships.dex.data.id',),
                          'base_token_id': ('relationships.base_token.data.id',),
                          'quote_token_id': ('relationships.quote_token.data.id',),
                          }])
        top_pools_by_network = glom(response, spec)
        return pd.DataFrame(top_pools_by_network)

    def get_top_pools_by_network_sync(self, network_id: str) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_top_pools_by_network(network_id))

    async def get_top_pools_by_network_dex(self, network_id: str, dex_id: str) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_TOP_POOLS_BY_NETWORK_DEX_PATH.format(network_id, dex_id))
        spec = ('data', [{'id': 'id', 'type': 'type',
                          'name': ('attributes.name',),
                          "base_token_price_usd": ("attributes.base_token_price_usd",),
                          "base_token_price_native_currency": ("attributes.base_token_price_native_currency",),
                          "quote_token_price_usd": ("attributes.quote_token_price_usd",),
                          "quote_token_price_native_currency": ("attributes.quote_token_price_native_currency",),
                          "address": ("attributes.address",),
                          "reserve_in_usd": ("attributes.reserve_in_usd",),
                          "pool_created_at": ("attributes.pool_created_at",),
                          "fdv_usd": ("attributes.fdv_usd",),
                          "market_cap_usd": ("attributes.market_cap_usd",),
                          "price_change_percentage_h1": ("attributes.price_change_percentage.h1",),
                          "price_change_percentage_h24": ("attributes.price_change_percentage.h24",),
                          "transactions_h1_buys": ("attributes.transactions.h1.buys",),
                          "transactions_h1_sells": ("attributes.transactions.h1.sells",),
                          "transactions_h24_buys": ("attributes.transactions.h24.buys",),
                          "transactions_h24_sells": ("attributes.transactions.h24.sells",),
                          "volume_usd_h24": ("attributes.volume_usd.h24",),
                          'dex_id': ('relationships.dex.data.id',),
                          'base_token_id': ('relationships.base_token.data.id',),
                          'quote_token_id': ('relationships.quote_token.data.id',),
                          }])
        top_pools_by_dex = glom(response, spec)
        return pd.DataFrame(top_pools_by_dex)

