# GeckoTerminal Py

GeckoTerminal Py is a Python client for the [GeckoTerminal](https://www.geckoterminal.com). It provides a user-friendly way to fetch network and pool data asynchronously or synchronously.

## Installation

To install GeckoTerminal Py, use pip:

```bash
pip install geckoterminal-py
```

## Usage

You can fetch data about networks using GeckoTerminal Py in two ways:

### Asynchronous usage

```python
from geckoterminal_py import GeckoTerminalAsyncClient
import asyncio


async def main():
    client = GeckoTerminalAsyncClient()
    networks_df = await client.get_networks()
    print(networks_df)
    await client.close()


# In an asyncio environment, you'd use:
asyncio.run(main())
```

### Synchronous usage

```python
from geckoterminal_py import GeckoTerminalSyncClient


def main():
    client = GeckoTerminalSyncClient()
    networks_df = client.get_networks()
    print(networks_df)
    client.close()


main()
```

## Methods Available

Here is a brief description of the methods available in the GeckoTerminalClient:
Please check the examples notebook where you can find the usage of all of them.

Methods:
- **get_networks():**
- **get_dexes_by_network(network_id: str):**
- **get_top_pools_by_network(network_id: str):**
- **get_top_pools_by_network_dex(network_id: str, dex_id: str):**
- **get_top_pools_by_network_token(network_id: str, token_id: str):**
- **get_new_pools_by_network(network_id: str):**
- **get_new_pools_all_networks():**
- **get_ohlcv(network_id: str, pool_address: str, timeframe: str, before_timestamp: int = None, currency: str = "usd", token: str = "base", limit: int = 1000):**

Endpoints to add:
- [ ] /simple/networks/{network}/token_price/{addresses}
- [ ] /search/pools
- [ ] / rest of tokens list