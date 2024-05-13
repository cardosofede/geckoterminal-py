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

    @staticmethod
    def get_timeframe_and_period(timeframe: str) -> (str, str):
        unit_conversion = {
            "m": "minute",
            "h": "hour",
            "d": "day",
        }
        period, unit = timeframe[:-1], timeframe[-1]
        return unit_conversion[unit], period
