import pandas as pd
import pytest
from aioresponses import aioresponses

from geckoterminal_py.client import GeckoTerminalClient
from tests.utils import get_response_from_file


@pytest.fixture
def mock_api():
    with aioresponses() as mock_api:
        yield mock_api


@pytest.fixture
def client():
    client = GeckoTerminalClient()
    yield client
    client.close()


class TestGeckoTerminalPyClient:
    networks_columns = ['id', 'type', 'name', 'coingecko_asset_platform_id']
    dexes_columns = ['id', 'type', 'name']
    pools_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                     'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                     'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                     'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                     'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                     'base_token_id', 'quote_token_id', 'network_id']

    @pytest.mark.asyncio
    async def test_get_networks(self, client, mock_api):
        response = get_response_from_file("get_networks")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks", payload=response)
        networks = await client.get_networks()
        assert isinstance(networks, pd.DataFrame)
        assert networks.columns.tolist() == self.networks_columns
        assert all(networks["type"] == "network")

    @pytest.mark.asyncio
    async def test_get_dexes_by_network(self, client, mock_api):
        response = get_response_from_file("get_dexes_by_network")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/ethereum/dexes", payload=response)
        dexes = await client.get_dexes_by_network(network_id="ethereum")
        assert isinstance(dexes, pd.DataFrame)
        assert dexes.columns.tolist() == self.dexes_columns
        assert all(dexes["type"] == "dex")

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/eth/pools", payload=response)
        top_pools = await client.get_top_pools_by_network(network_id="eth")
        assert isinstance(top_pools, pd.DataFrame)
        assert top_pools.columns.tolist() == self.pools_columns
        assert all(top_pools["network_id"] == "eth")

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network_dex(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network_dex")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/eth/dexes/sushiswap/pools", payload=response)
        top_pools = await client.get_top_pools_by_network_dex(network_id="eth", dex_id="sushiswap")
        assert isinstance(top_pools, pd.DataFrame)
        assert top_pools.columns.tolist() == self.pools_columns
        assert all(top_pools["network_id"] == "eth")
        assert all(top_pools["dex_id"] == "sushiswap")

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network_token(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network_token")
        mock_api.get(url="https://api.geckoterminal.com/api/v2/networks/eth/"
                         "tokens/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48/pools", payload=response)
        top_pools = await client.get_top_pools_by_network_token(network_id="eth",
                                                                token_id="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        assert isinstance(top_pools, pd.DataFrame)
        assert top_pools.columns.tolist() == self.pools_columns
        assert all(top_pools["network_id"] == "eth")
        assert all((top_pools["base_token_id"] == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48") |
                   (top_pools["quote_token_id"] == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"))

    @pytest.mark.asyncio
    async def test_get_ohlcv(self, client, mock_api):
        network_id = "eth"
        pool_address = "0x60594a405d53811d3bc4766596efd80fd545a270"
        timeframe = "15m"
        before_timestamp = 1689280680
        response = get_response_from_file("get_ohlcv")
        mock_api.get(url=f"https://api.geckoterminal.com/api/v2/networks/{network_id}/pools/{pool_address}"
                         f"/ohlcv/minute?aggregate=15&before_timestamp={before_timestamp}&currency=usd&limit=1000&token=base",
                     payload=response)
        ohlcv = await client.get_ohlcv(network_id=network_id, pool_address=pool_address, timeframe=timeframe,
                                       before_timestamp=before_timestamp)
        assert isinstance(ohlcv, pd.DataFrame)
        assert ohlcv.columns.tolist() == ["timestamp", "open", "high", "low", "close", "volume_usd", "datetime"]
        assert all(ohlcv["datetime"] < pd.to_datetime(before_timestamp, unit="s"))

    def test_get_networks_sync(self, client, mock_api):
        response = get_response_from_file("get_networks")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks", payload=response)
        networks = client.get_networks_sync()
        assert isinstance(networks, pd.DataFrame)
        assert networks.columns.tolist() == self.networks_columns
        assert all(networks["type"] == "network")

    def test_get_dexes_by_network_sync(self, client, mock_api):
        response = get_response_from_file("get_dexes_by_network")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/ethereum/dexes", payload=response)
        dexes = client.get_dexes_by_network_sync(network_id="ethereum")
        assert isinstance(dexes, pd.DataFrame)
        assert dexes.columns.tolist() == self.dexes_columns
        assert all(dexes["type"] == "dex")

    def test_get_top_pools_by_network_sync(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/eth/pools", payload=response)
        top_pools = client.get_top_pools_by_network_sync(network_id="eth")
        assert isinstance(top_pools, pd.DataFrame)
        assert top_pools.columns.tolist() == self.pools_columns
        assert all(top_pools["network_id"] == "eth")

    def test_get_top_pools_by_network_dex_sync(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network_dex")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/eth/dexes/sushiswap/pools", payload=response)
        top_pools = client.get_top_pools_by_network_dex_sync(network_id="eth", dex_id="sushiswap")
        assert isinstance(top_pools, pd.DataFrame)
        assert top_pools.columns.tolist() == self.pools_columns
        assert all(top_pools["network_id"] == "eth")
        assert all(top_pools["dex_id"] == "sushiswap")

    def test_get_top_pools_by_network_token_sync(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network_token")
        mock_api.get(url="https://api.geckoterminal.com/api/v2/networks/eth/"
                         "tokens/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48/pools", payload=response)
        top_pools = client.get_top_pools_by_network_token_sync(network_id="eth",
                                                               token_id="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        assert isinstance(top_pools, pd.DataFrame)
        assert top_pools.columns.tolist() == self.pools_columns
        assert all(top_pools["network_id"] == "eth")
        assert all((top_pools["base_token_id"] == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48") |
                   (top_pools["quote_token_id"] == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"))

    def test_get_ohlcv_sync(self, client, mock_api):
        response = get_response_from_file("get_ohlcv")
        mock_api.get(url="https://api.geckoterminal.com/api/v2/networks/eth/pools/"
                         "0x60594a405d53811d3bc4766596efd80fd545a270/ohlcv/minute?aggregate=15&before_timestamp=1689280680&currency=usd&limit=1000&token=base",
                     payload=response)
        ohlcv = client.get_ohlcv_sync(network_id="eth", pool_address="0x60594a405d53811d3bc4766596efd80fd545a270",
                                      timeframe="15m", before_timestamp=1689280680)
        assert isinstance(ohlcv, pd.DataFrame)
        assert ohlcv.columns.tolist() == ["timestamp", "open", "high", "low", "close", "volume_usd", "datetime"]
        assert all(ohlcv["datetime"] < pd.to_datetime(1689280680, unit="s"))

    @pytest.mark.asyncio
    async def test_ohlcv_raises_exception_timeframe(self, client):
        timeframe = "16m"
        with pytest.raises(ValueError) as timeframe_error:
            await client.get_ohlcv(network_id="eth", pool_address="0x60594a405d53811d3bc4766596efd80fd545a270",
                                   timeframe=timeframe)
            assert f"Timeframe {timeframe} is not supported." in str(timeframe_error.value)
