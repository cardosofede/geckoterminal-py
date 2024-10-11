from typing import Optional

import httpx
import pandas as pd
from glom import glom

from geckoterminal_py.base_client import GeckoTerminalClientBase
import geckoterminal_py.constants as CONSTANTS


class GeckoTerminalSyncClient(GeckoTerminalClientBase):
    def __init__(self, transport: Optional[httpx.MockTransport] = None):
        if transport:
            self.client = httpx.Client(headers=self.headers, transport=transport)
        else:
            self.client = httpx.Client(headers=self.headers)

    def api_request(self, method: str, path: str, params: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{path}"
        response = self.client.request(method, url, params=params)
        response.raise_for_status()
        return response.json()

    def close(self):
        self.client.close()

    def get_networks(self) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_NETWORKS_PATH)
        networks = glom(response, CONSTANTS.NETWORK_SPEC)
        return pd.DataFrame(networks)

    def get_dexes_by_network(self, network_id: str) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_DEXES_BY_NETWORK_PATH.format(network_id))
        dexes_by_network = glom(response, CONSTANTS.DEXES_BY_NETWORK_SPEC)
        return pd.DataFrame(dexes_by_network)

    def get_top_pools_by_network(self, network_id: str) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_TOP_POOLS_BY_NETWORK_PATH.format(network_id))
        top_pools_by_network = glom(response, CONSTANTS.POOL_SPEC)
        return self.process_pools_list(top_pools_by_network)

    def get_top_pools_by_network_dex(self, network_id: str, dex_id: str) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_TOP_POOLS_BY_NETWORK_DEX_PATH.format(network_id, dex_id))
        top_pools_by_dex = glom(response, CONSTANTS.POOL_SPEC)
        return self.process_pools_list(top_pools_by_dex)

    def get_top_pools_by_network_token(self, network_id: str, token_id: str) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_TOP_POOLS_BY_NETWORK_TOKEN_PATH.format(network_id, token_id))
        top_pools_by_token = glom(response, CONSTANTS.POOL_SPEC)
        return self.process_pools_list(top_pools_by_token)

    def get_new_pools_by_network(self, network_id: str) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_NEW_POOLS_BY_NETWORK_PATH.format(network_id))
        new_pools_by_network = glom(response, CONSTANTS.POOL_SPEC)
        return self.process_pools_list(new_pools_by_network)

    def get_new_pools_all_networks(self) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_NEW_POOLS_ALL_NETWORKS_PATH)
        new_pools_all_networks = glom(response, CONSTANTS.POOL_SPEC)
        return self.process_pools_list(new_pools_all_networks)

    def get_pool_by_network_address(self, network_id: str, pool_address: str) -> pd.DataFrame:
        response = self.api_request("GET", CONSTANTS.GET_POOL_BY_NETWORK_AND_ADDRESS_PATH.format(network_id, pool_address))
        pool = glom(response, CONSTANTS.POOL_SPEC)
        return pd.DataFrame(pool)

    def get_ohlcv(self, network_id: str, pool_address: str, timeframe: str, before_timestamp: int = None,
                  currency: str = "usd", token: str = "base", limit: int = 1000) -> pd.DataFrame:
        if timeframe not in self.ohlcv_timeframes:
            raise ValueError(f"Timeframe {timeframe} is not supported. Please select one timeframe of the following"
                             f"list {self.ohlcv_timeframes}")
        timeframe, period = self.get_timeframe_and_period(timeframe)
        params = {
            "aggregate": period,
            "limit": limit,
            "currency": currency,
            "token": token,
        }
        if before_timestamp:
            params["before_timestamp"] = before_timestamp
        response = self.api_request("GET",
                                    CONSTANTS.GET_OHLCV_DATA_PATH.format(network_id, pool_address, timeframe),
                                    params=params)

        df = pd.DataFrame(response["data"]["attributes"]["ohlcv_list"],
                          columns=["timestamp", "open", "high", "low", "close", "volume_usd"])
        df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
        return df.drop_duplicates(subset="timestamp").sort_values("datetime").reset_index(drop=True)

