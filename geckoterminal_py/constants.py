# Networks
GET_NETWORKS_PATH = "networks"

# Dexes
GET_DEXES_BY_NETWORK_PATH = "networks/{}/dexes"

# Pools
GET_POOL_BY_NETWORK_AND_ADDRESS_PATH = "networks/{}/pools/{}"
GET_TOP_POOLS_BY_NETWORK_PATH = "networks/{}/pools"
GET_TOP_POOLS_BY_NETWORK_DEX_PATH = "networks/{}/dexes/{}/pools"
GET_NEW_POOLS_BY_NETWORK_PATH = "networks/{}/new_pools"
GET_NEW_POOLS_ALL_NETWORKS_PATH = "networks/new_pools"
GET_POOL_BY_NETWORK_PATH = "networks/{}/pools/{}"

# Tokens
GET_TOP_POOLS_BY_NETWORK_TOKEN_PATH = "networks/{}/tokens/{}/pools"
GET_SPECIFIC_TOKEN_ON_NETWORK_PATH = "networks/{}/tokens/{}"

# OHLCV
GET_OHLCV_DATA_PATH = "networks/{}/pools/{}/ohlcv/{}"

# GLOM SPECS

POOL_SPEC = ('data', [{'id': 'id', 'type': 'type',
                       'name': ('attributes.name',),
                       "base_token_price_usd": ("attributes.base_token_price_usd",),
                       "base_token_price_native_currency": ("attributes.base_token_price_native_currency",),
                       "quote_token_price_usd": ("attributes.quote_token_price_usd",),
                       "quote_token_price_native_currency": ("attributes.quote_token_price_native_currency",),
                       "address": ("attributes.address",),
                       "reserve_in_usd": ("attributes.reserve_in_usd",),
                       "pool_created_at": ("attributes.pool_created_at",),
                       "fdv_usd": ("attributes.fdv_usd",),
                       "market_cap_usd": ("attributes.market_cap_usd",),
                       "price_change_percentage_h1": ("attributes.price_change_percentage.h1",),
                       "price_change_percentage_h24": ("attributes.price_change_percentage.h24",),
                       "transactions_h1_buys": ("attributes.transactions.h1.buys",),
                       "transactions_h1_sells": ("attributes.transactions.h1.sells",),
                       "transactions_h24_buys": ("attributes.transactions.h24.buys",),
                       "transactions_h24_sells": ("attributes.transactions.h24.sells",),
                       "volume_usd_h24": ("attributes.volume_usd.h24",),
                       'dex_id': ('relationships.dex.data.id',),
                       'base_token_id': ('relationships.base_token.data.id',),
                       'quote_token_id': ('relationships.quote_token.data.id',),
                       }])

NETWORK_SPEC = ('data', [{'id': 'id', 'type': 'type', 'name': ('attributes.name',),
                          'coingecko_asset_platform_id': ('attributes.coingecko_asset_platform_id',)}])

DEXES_BY_NETWORK_SPEC = ('data', [{'id': 'id', 'type': 'type', 'name': ('attributes.name',)}])
