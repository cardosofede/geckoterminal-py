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
- **get_simple_token_price(network_id: str, token_addresses: list, include_market_cap: bool = False, mcap_fdv_fallback: bool = False, include_24hr_vol: bool = False, include_24hr_price_change: bool = False, include_total_reserve_in_usd: bool = False):** Fetch USD prices for up to 30 token addresses in a single call. Returns a DataFrame keyed by `token_address` with a `price_usd` column (plus optional `market_cap_usd` / `volume_usd_h24` / `price_change_percentage_h24` / `reserve_in_usd` columns when requested).

Endpoints to add:
- [ ] /search/pools
- [ ] / rest of tokens list