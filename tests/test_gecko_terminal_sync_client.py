import asyncio
import pandas as pd
import pytest
import httpx
from httpx import Request, Response
from geckoterminal_py import GeckoTerminalAsyncClient, GeckoTerminalSyncClient


# Helper function to load JSON data from a file.
def load_json(filename):
    """Load JSON data from a file."""
    import json
    with open(filename, 'r') as file:
        return json.load(file)


# Synchronous request handler for mocking HTTP responses based on the requested URL.
def unified_request_handler(request: Request) -> Response:
    """A unified request handler for HTTPX MockTransport to mock API responses.

    Args:
        request: The HTTP request object.

    Returns:
        An HTTPX Response object with the mocked data or an error response if the path is not found.
    """
    # Mapping of API endpoint paths to corresponding JSON response files.
    path_to_json = {
        "/api/v2/networks": "test_data/get_networks.json",
        "/api/v2/networks/eth/dexes": "test_data/get_dexes_by_network.json",
        "/api/v2/networks/eth/pools": "test_data/get_top_pools_by_network.json",
        "/api/v2/networks/eth/tokens/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/pools": "test_data/get_top_pools_by_network_token.json",
        "/api/v2/networks/eth/dexes/sushiswap/pools": "test_data/get_top_pools_by_network_dex.json",
        "/api/v2/networks/eth/new_pools": "test_data/get_new_pools_by_network.json",
        "/api/v2/networks/new_pools": "test_data/get_new_pools_all_networks.json",
        "/api/v2/networks/eth/pools/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/ohlcv/hour": "test_data/get_ohlcv.json"
    }

    json_file = path_to_json.get(request.url.path)
    if json_file:
        data = load_json(json_file)
        return httpx.Response(200, json=data)
    return httpx.Response(404, json={"error": "not found"})


@pytest.fixture
def client():
    """Pytest fixture to provide a GeckoTerminalAsyncClient instance with a mocked HTTP transport."""
    transport = httpx.MockTransport(unified_request_handler)
    test_client = GeckoTerminalSyncClient(transport=transport)
    yield test_client
    test_client.close()


class TestGeckoTerminalSyncClient:
    """Test suite for GeckoTerminalSyncClient."""

    def test_get_networks(self, client):
        """Test fetching networks and validate the structure and type of response."""
        networks =  client.get_networks()
        assert isinstance(networks, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'coingecko_asset_platform_id']
        assert list(networks.columns) == expected_columns
        assert all(networks['type'] == 'network')

    def test_get_dexes_by_network(self, client):
        """Test fetching decentralized exchanges by network and validate the response."""
        dexes =  client.get_dexes_by_network(network_id="eth")
        assert isinstance(dexes, pd.DataFrame)
        expected_columns = ['id', 'type', 'name']
        assert list(dexes.columns) == expected_columns
        assert all(dexes['type'] == 'dex')

    def test_get_top_pools_by_network(self, client):
        """Test fetching top pools by network and validate the response."""
        top_pools = client.get_top_pools_by_network(network_id="eth")
        assert isinstance(top_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(top_pools.columns) == expected_columns
        assert all(top_pools['network_id'] == 'eth')

    def test_get_top_pools_by_network_dex(self, client):
        """Test fetching top pools by network and DEX and validate the response."""
        top_pools = client.get_top_pools_by_network_dex(network_id="eth", dex_id="sushiswap")
        assert isinstance(top_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(top_pools.columns) == expected_columns
        assert all(top_pools['network_id'] == 'eth')
        assert all(top_pools['dex_id'] == 'sushiswap')

    def test_get_top_pools_by_network_token(self, client):
        """Test fetching top pools by network and token and validate the response."""
        token_id = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        top_pools = client.get_top_pools_by_network_token(network_id="eth", token_id=token_id)
        assert isinstance(top_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(top_pools.columns) == expected_columns
        assert all(top_pools['network_id'] == 'eth')

    def test_get_new_pools_all_networks(self, client):
        """Test fetching new pools across all networks and validate the response."""
        new_pools = client.get_new_pools_all_networks()
        assert isinstance(new_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(new_pools.columns) == expected_columns

    def test_get_new_pools_by_network(self, client):
        """Test fetching new pools by network and validate the response."""
        new_pools = client.get_new_pools_by_network(network_id="eth")
        assert isinstance(new_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(new_pools.columns) == expected_columns
        assert all(new_pools['network_id'] == 'eth')

    def test_get_ohlcv(self, client):
        """Test fetching OHLCV data for a pool and validate the response."""
        ohlcv = client.get_ohlcv(network_id="eth", pool_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", timeframe="1h")
        assert isinstance(ohlcv, pd.DataFrame)
        expected_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume_usd', 'datetime']
        assert list(ohlcv.columns) == expected_columns
