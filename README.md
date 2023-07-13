# GeckoTerminal Py

GeckoTerminal Py is a Python client for the [GeckoTerminal API](https://api.geckoterminal.com/api/v2). It provides a user-friendly way to fetch network and pool data asynchronously or synchronously.

## Installation

To install GeckoTerminal Py, use pip:

```bash
pip install geckoterminal-py
```

## Usage

You can fetch data about networks using GeckoTerminal Py in two ways:

### Asynchronous usage


```python
from geckoterminal_py.client import GeckoTerminalClient
import asyncio


async def main():
    client = GeckoTerminalClient()
    networks_df = await client.get_networks()
    print(networks_df)

# In an asyncio environment, you'd use:
asyncio.run(main())
```

### Synchronous usage

```python
from geckoterminal_py.client import GeckoTerminalClient

def main():
    client = GeckoTerminalClient()
    networks_df = client.get_networks_sync()
    print(networks_df)

main()
```

## Methods Available

Here is a brief description of the methods available in the GeckoTerminalClient:

Async methods:
- **get_networks():** Fetches network data in an asynchronous way.
- **get_dexes_by_network(network_id: str):** Asynchronously fetches decentralized exchange (dex) data by network ID.
- **get_top_pools_by_network(network_id: str):** Asynchronously fetches top pool data by network ID.
- **get_top_pools_by_network_dex(network_id: str, dex_id: str):** Asynchronously fetches top pool data by network and dex IDs.
- **get_top_pools_by_network_token(network_id: str, token_id: str):** Asynchronously fetches top pool data by network and token IDs.
- **get_new_pools_by_network(network_id: str):** Asynchronously fetches data of new pools by network ID.
- **get_new_pools_all_networks():** Asynchronously fetches data of new pools across all networks.
- **get_ohlcv(network_id: str, pool_address: str, timeframe: str, before_timestamp: int = None, currency: str = "usd", token: str = "base", limit: int = 1000):** Asynchronously fetches OHLCV data for a pool.

Sync methods:
- **get_networks_sync():** Fetches network data in a synchronous way.
- **get_dexes_by_network_sync(network_id: str):** Synchronously fetches dex data by network ID.
- **get_top_pools_by_network_sync(network_id: str):** Synchronously fetches top pool data by network ID.
- **get_top_pools_by_network_dex_sync(network_id: str, dex_id: str):** Synchronously fetches top pool data by network and dex IDs.
- **get_top_pools_by_network_token_sync(network_id: str, token_id: str):** Synchronously fetches top pool data by network and token IDs.
- **get_new_pools_by_network_sync(network_id: str):** Synchronously fetches data of new pools by network ID.
- **get_new_pools_all_networks_sync():** Synchronously fetches data of new pools across all networks.
- **get_ohlcv_sync(network_id: str, pool_address: str, timeframe: str, before_timestamp: int = None, currency: str = "usd", token: str = "base", limit: int = 1000):** Synchronously fetches OHLCV data for a pool.