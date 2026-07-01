from typing import Dict, List
import pandas as pd


class GeckoTerminalClientBase:
    headers = {
        "Accept": "application/json;version=20230302",
    }
    base_url = "https://api.geckoterminal.com/api/v2"
    ohlcv_timeframes = ["1m", "5m", "15m", "1h", "4h", "12h", "1d"]

    @staticmethod
    def process_pools_list(pools_list: List[Dict[str, str]]) -> pd.DataFrame:
        df = pd.DataFrame(pools_list)
        df["network_id"] = df["id"].apply(lambda x: x.split("_")[0])
        df["quote_token_id"] = df["quote_token_id"].apply(lambda x: x.split("_")[1])
        df["base_token_id"] = df["base_token_id"].apply(lambda x: x.split("_")[1])
        return df

    # Optional attribute maps returned by the simple token price endpoint, mapped to the
    # column names already used across the pool DataFrames so downstream code stays consistent.
    SIMPLE_TOKEN_PRICE_OPTIONAL_FIELDS = {
        "market_cap_usd": "market_cap_usd",
        "h24_volume_usd": "volume_usd_h24",
        "h24_price_change_percentage": "price_change_percentage_h24",
        "total_reserve_in_usd": "reserve_in_usd",
    }

    @classmethod
    def process_simple_token_price(cls, response: Dict) -> pd.DataFrame:
        """Flatten a simple token price response into a DataFrame keyed by token address.

        Always yields a ``token_address``/``price_usd`` frame; the optional maps (market cap,
        24h volume, 24h price change, total reserve) are added as extra columns only when the
        request asked for them and the API returned them.
        """
        attributes = response.get("data", {}).get("attributes", {}) or {}
        token_prices = attributes.get("token_prices", {}) or {}
        df = pd.DataFrame(
            [{"token_address": address, "price_usd": price} for address, price in token_prices.items()],
            columns=["token_address", "price_usd"],
        )
        for source_field, column in cls.SIMPLE_TOKEN_PRICE_OPTIONAL_FIELDS.items():
            values = attributes.get(source_field)
            if isinstance(values, dict):
                df[column] = df["token_address"].map(values)
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
