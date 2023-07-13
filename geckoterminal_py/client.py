import asyncio
from typing import Optional, Dict, List
from glom import glom
import pandas as pd

import aiohttp

import geckoterminal_py.constants as CONSTANTS


class GeckoTerminalClient:
    # TODO: Implement get pool by network and pool id
    # TODO: Implement get specific token in network
    base_url = "https://api.geckoterminal.com/api/v2"
    headers = {
        "Accept": "application/json;version=20230302",
    }
    ohlcv_timeframes = ["1m", "5m", "15m", "1h", "4h", "12h", "1d"]

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

    @property
    def glom_pool_spec(self):
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
        return spec

    @staticmethod
    def process_pools_list(pools_list: List[Dict[str, str]]) -> pd.DataFrame:
        df = pd.DataFrame(pools_list)
        df["network_id"] = df["id"].apply(lambda x: x.split("_")[0])
        df["quote_token_id"] = df["quote_token_id"].apply(lambda x: x.split("_")[1])
        df["base_token_id"] = df["base_token_id"].apply(lambda x: x.split("_")[1])
        return df

    @staticmethod
    def get_timeframe_and_period(timeframe: str) -> (str, str):
        unit_conversion = {
            "m": "minute",
            "h": "hour",
            "d": "day",
        }
        period, unit = timeframe[:-1], timeframe[-1]
        return unit_conversion[unit], period

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
        top_pools_by_network = glom(response, self.glom_pool_spec)
        return self.process_pools_list(top_pools_by_network)

    def get_top_pools_by_network_sync(self, network_id: str) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_top_pools_by_network(network_id))

    async def get_top_pools_by_network_dex(self, network_id: str, dex_id: str) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_TOP_POOLS_BY_NETWORK_DEX_PATH.format(network_id, dex_id))
        top_pools_by_dex = glom(response, self.glom_pool_spec)
        return self.process_pools_list(top_pools_by_dex)

    def get_top_pools_by_network_dex_sync(self, network_id: str, dex_id: str) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_top_pools_by_network_dex(network_id, dex_id))

    async def get_top_pools_by_network_token(self, network_id: str, token_id: str) -> pd.DataFrame:
        response = await self.api_request("GET",
                                          CONSTANTS.GET_TOP_POOLS_BY_NETWORK_TOKEN_PATH.format(network_id, token_id))
        top_pools_by_token = glom(response, self.glom_pool_spec)
        return self.process_pools_list(top_pools_by_token)

    def get_top_pools_by_network_token_sync(self, network_id: str, token_id: str) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_top_pools_by_network_token(network_id, token_id))

    async def get_new_pools_by_network(self, network_id: str) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_NEW_POOLS_BY_NETWORK_PATH.format(network_id))
        new_pools_by_network = glom(response, self.glom_pool_spec)
        return self.process_pools_list(new_pools_by_network)

    def get_new_pools_by_network_sync(self, network_id: str) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_new_pools_by_network(network_id))

    async def get_new_pools_all_networks(self) -> pd.DataFrame:
        response = await self.api_request("GET", CONSTANTS.GET_NEW_POOLS_ALL_NETWORKS_PATH)
        new_pools_all_networks = glom(response, self.glom_pool_spec)
        return self.process_pools_list(new_pools_all_networks)

    def get_new_pools_all_networks_sync(self) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_new_pools_all_networks())

    async def get_ohlcv(self, network_id: str, pool_address: str, timeframe: str, before_timestamp: int = None,
                        currency: str = "usd", token: str = "base", limit: int = 1000) -> pd.DataFrame:
        timeframe, period = self.get_timeframe_and_period(timeframe)
        response = await self.api_request("GET",
                                          CONSTANTS.GET_OHLCV_DATA_PATH.format(network_id,
                                                                               pool_address,
                                                                               timeframe),
                                          params={
                                              "before_timestamp": before_timestamp,
                                              "aggregate": period,
                                              "limit": limit,
                                              "currency": currency,
                                              "token": token,
                                          })

        df = pd.DataFrame(response["data"]["attributes"]["ohlcv_list"],
                          columns=["timestamp", "open", "high", "low", "close", "volume_usd"])
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
        return df.drop_duplicates(subset="timestamp").sort_values("datetime").reset_index(drop=True)

    def get_ohlcv_sync(self, network_id: str, pool_address: str, timeframe: str, before_timestamp: int = None,
                       currency: str = "usd", token: str = "base", limit: int = 1000) -> pd.DataFrame:
        return self.ev_loop.run_until_complete(self.get_ohlcv(network_id, pool_address, timeframe, before_timestamp,
                                                              currency, token, limit))
