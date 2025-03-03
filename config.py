from fake_useragent import FakeUserAgent



TOKEN = ...

user_agent = FakeUserAgent().random
HEADER = {
    'accept': 'application/json, text/plain, */*',
    'user-agent': user_agent
}

ALLOWED_TOKENS = [
    'bitcoin', 'ethereum', 'xrp', 'tether', 'solana', 'bnb', 
    'usd-coin', 'dogecoin', 'cardano','stellar', 'unus-sed-leo', 
    'tron', 'chainlink', 'avalanche', 'toncoin', 'hyperliquid', 
    'sui', 'hedera', 'shiba-inu', 'polkadot-new', 'ethena-usde',
    'litecoin', 'bitget-token-new', 'bitcoin-cash', 'near-protocol', 
    'uniswap', 'pepe', 'official-trump', 'multi-collateral-dai',
    'aave', 'aptos', 'ethereum-classic', 'monero', 'mantle',
    'vechain', 'cronos', 'polygon-ecosystem-token', 'kaspa',
    'algorand', 'okb', 'filecoin', 'cosmos', 'bittensor', 'arbitrum'
    'gatetoken', 'gala', 'kaia', 'eos', 'tezos', 'iota', 'quant',
    'aioz-network', 'polygon', 'apecoin-ape', 'tether-gold'
]

ALLOWED_EXCHANGERS = [
    'Bybit', 'OKX', 'Bitget', 'KuCoin', 'MEXC',
    'Bitfinex', 'Gate.io','BingX', 'XT.com', 
    'Bitrue', 'CoinEx', 'Poloniex', 'Bitget', 'Kraken',
    'Bittrex', 'LATOKEN', 'Phemex', 'Upbit', 'CEX.IO', 'Dex-Trade', 'LBank',
    'Pionex', 'BigONE', 'Coinstore', 'DigiFinex', 'Giottus', 'XT.COM', 'Bitstamp',
    'CoinW', 'EXMO.ME', 'KuCoin', 'Tidex'
]

COMMAND_ERROR_MESSAGE = \
"""
❌ Команда не распознана

Для начала работы с ботом используйте команду /start
"""

CONTACTS_INFO = "<b>Поддержка:</b>\n- @CryptoBlackrock_Support"

INFO = \
"""
Этот бот предоставляет широкий функционал для поиска криптоарбитражных сделок на основе более чем 10к+ монет!  ✅\n
⚠️ Бот не является финансовой рекомендацией! Выполняйте все действия на свой страх и риск  ⚠️"""

DEVLOG = \
"""
11.02
 - добавлен обьем к арбитражам
 - форматирование дат и времени
 - добавлена сортировка по профиту
 - добавлен маркер для показателя ликвидности
 - начата разработка базы данных
"""