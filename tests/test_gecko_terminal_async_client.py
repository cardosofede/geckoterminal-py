import asyncio
import pandas as pd
import pytest
import httpx
from httpx import Request, Response
from geckoterminal_py import GeckoTerminalAsyncClient


# Helper function to load JSON data from a file.
def load_json(filename):
    """Load JSON data from a file."""
    import json
    with open(filename, 'r') as file:
        return json.load(file)


# Asynchronous request handler for mocking HTTP responses based on the requested URL.
async def unified_request_handler(request: Request) -> Response:
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
        "/api/v2/networks/eth/pools/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/ohlcv/hour": "test_data/get_ohlcv.json",
        "/api/v2/simple/networks/eth/token_price/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": "test_data/get_simple_token_price.json",
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
    test_client = GeckoTerminalAsyncClient(transport=transport)
    yield test_client
    asyncio.run(test_client.close())


class TestGeckoTerminalAsyncClient:
    """Test suite for GeckoTerminalAsyncClient."""

    @pytest.mark.asyncio
    async def test_get_networks(self, client):
        """Test fetching networks and validate the structure and type of response."""
        networks = await client.get_networks()
        assert isinstance(networks, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'coingecko_asset_platform_id']
        assert list(networks.columns) == expected_columns
        assert all(networks['type'] == 'network')

    @pytest.mark.asyncio
    async def test_get_dexes_by_network(self, client):
        """Test fetching decentralized exchanges by network and validate the response."""
        dexes = await client.get_dexes_by_network(network_id="eth")
        assert isinstance(dexes, pd.DataFrame)
        expected_columns = ['id', 'type', 'name']
        assert list(dexes.columns) == expected_columns
        assert all(dexes['type'] == 'dex')

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network(self, client):
        """Test fetching top pools by network and validate the response."""
        top_pools = await client.get_top_pools_by_network(network_id="eth")
        assert isinstance(top_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(top_pools.columns) == expected_columns
        assert all(top_pools['network_id'] == 'eth')

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network_dex(self, client):
        """Test fetching top pools by network and DEX and validate the response."""
        top_pools = await client.get_top_pools_by_network_dex(network_id="eth", dex_id="sushiswap")
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

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network_token(self, client):
        """Test fetching top pools by network and token and validate the response."""
        token_id = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        top_pools = await client.get_top_pools_by_network_token(network_id="eth", token_id=token_id)
        assert isinstance(top_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(top_pools.columns) == expected_columns
        assert all(top_pools['network_id'] == 'eth')

    @pytest.mark.asyncio
    async def test_get_new_pools_all_networks(self, client):
        """Test fetching new pools across all networks and validate the response."""
        new_pools = await client.get_new_pools_all_networks()
        assert isinstance(new_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(new_pools.columns) == expected_columns

    @pytest.mark.asyncio
    async def test_get_new_pools_by_network(self, client):
        """Test fetching new pools by network and validate the response."""
        new_pools = await client.get_new_pools_by_network(network_id="eth")
        assert isinstance(new_pools, pd.DataFrame)
        expected_columns = ['id', 'type', 'name', 'base_token_price_usd', 'base_token_price_native_currency',
                            'quote_token_price_usd', 'quote_token_price_native_currency', 'address', 'reserve_in_usd',
                            'pool_created_at', 'fdv_usd', 'market_cap_usd', 'price_change_percentage_h1',
                            'price_change_percentage_h24', 'transactions_h1_buys', 'transactions_h1_sells',
                            'transactions_h24_buys', 'transactions_h24_sells', 'volume_usd_h24', 'dex_id',
                            'base_token_id', 'quote_token_id', 'network_id']
        assert list(new_pools.columns) == expected_columns
        assert all(new_pools['network_id'] == 'eth')

    @pytest.mark.asyncio
    async def test_get_ohlcv(self, client):
        """Test fetching OHLCV data for a pool and validate the response."""
        ohlcv = await client.get_ohlcv(network_id="eth", pool_address="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", timeframe="1h")
        assert isinstance(ohlcv, pd.DataFrame)
        expected_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume_usd', 'datetime']
        assert list(ohlcv.columns) == expected_columns

    @pytest.mark.asyncio
    async def test_get_simple_token_price(self, client):
        """Test fetching simple token prices for multiple addresses in a single call."""
        prices = await client.get_simple_token_price(
            network_id="eth",
            token_addresses=["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                             "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"],
            include_market_cap=True,
            include_24hr_vol=True,
            include_24hr_price_change=True,
            include_total_reserve_in_usd=True,
        )
        assert isinstance(prices, pd.DataFrame)
        expected_columns = ['token_address', 'price_usd', 'market_cap_usd', 'volume_usd_h24',
                            'price_change_percentage_h24', 'reserve_in_usd']
        assert list(prices.columns) == expected_columns
        assert len(prices) == 2
        weth = prices.set_index("token_address").loc["0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"]
        assert weth["price_usd"] == "2958.19885153499"
        assert weth["volume_usd_h24"] == "1200000000"

    @pytest.mark.asyncio
    async def test_get_simple_token_price_empty(self, client):
        """An empty address list returns an empty frame without hitting the API."""
        prices = await client.get_simple_token_price(network_id="eth", token_addresses=[])
        assert isinstance(prices, pd.DataFrame)
        assert list(prices.columns) == ['token_address', 'price_usd']
        assert prices.empty

    @pytest.mark.asyncio
    async def test_get_simple_token_price_too_many(self, client):
        """Requesting more than the per-call address limit raises a ValueError."""
        with pytest.raises(ValueError):
            await client.get_simple_token_price(network_id="eth", token_addresses=[str(i) for i in range(31)])
