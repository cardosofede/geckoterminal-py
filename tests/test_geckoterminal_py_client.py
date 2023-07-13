import json

import pandas as pd
import pytest
from glom import glom
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

    @pytest.mark.asyncio
    async def test_get_networks(self, client, mock_api):
        response = get_response_from_file("get_networks")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks", payload=response)
        networks = await client.get_networks()
        assert isinstance(networks, pd.DataFrame)
        assert networks.columns.tolist() == ['id', 'type', 'name', 'coingecko_asset_platform_id']
        assert all(networks["type"] == "network")

    @pytest.mark.asyncio
    async def test_get_dexes_by_network(self, client, mock_api):
        response = get_response_from_file("get_dexes_by_network")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/ethereum/dexes", payload=response)
        dexes = await client.get_dexes_by_network(network_id="ethereum")
        assert isinstance(dexes, pd.DataFrame)
        assert dexes.columns.tolist() == ['id', 'type', 'name']
        assert all(dexes["type"] == "dex")

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/eth/pools", payload=response)
        top_pools = await client.get_top_pools_by_network(network_id="eth")
        assert isinstance(top_pools, pd.DataFrame)
        assert "id" in top_pools.columns.tolist()
        assert "type" in top_pools.columns.tolist()
        assert "name" in top_pools.columns.tolist()
        assert "base_token_price_usd" in top_pools.columns.tolist()
        assert "quote_token_price_usd" in top_pools.columns.tolist()

    @pytest.mark.asyncio
    async def test_get_top_pools_by_network_dex(self, client, mock_api):
        response = get_response_from_file("get_top_pools_by_network_dex")
        mock_api.get("https://api.geckoterminal.com/api/v2/networks/eth/dexes/sushiswap/pools", payload=response)
        top_pools = await client.get_top_pools_by_network_dex(network_id="eth", dex_id="sushiswap")
        assert isinstance(top_pools, pd.DataFrame)
        assert "id" in top_pools.columns.tolist()
        assert "type" in top_pools.columns.tolist()
        assert "name" in top_pools.columns.tolist()
        assert "base_token_price_usd" in top_pools.columns.tolist()
        assert "quote_token_price_usd" in top_pools.columns.tolist()
