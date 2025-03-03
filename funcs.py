import os
import csv
import json
import config
import requests
from datetime import datetime
from zoneinfo import ZoneInfo



ARBITRAGES = []



def userExist(tgid: int) -> bool:
    with open('data/users/users.csv', 'r', encoding='utf-8') as users:
        for line in users.readlines():
            if tgid == int(line.split('|')[1]):
                return True
        return False



def addUser(login: str, tgid: int, name: str) -> bool:
    if userExist(tgid):
        return  
    with open('data/users/users.csv', 'a', encoding='utf-8', newline='') as storage:
        writer = csv.writer(
            storage,
            delimiter='|',
            quoting=csv.QUOTE_STRINGS,
        )

        writer.writerow([login]+[tgid]+[name])



def percentage_difference(num1, num2) -> float:
    """функция возвращает процентное отличие между двумя числами"""
    num1 = float(num1)
    num2 = float(num2)
    return round(
        (( (num1 - num2) / num2 ) * 100),
        2
    )



def update_data() -> None:
    global ARBITRAGES

    for filename in os.listdir('data/tokenPairs'):
        os.remove(f'data/tokenPairs/{filename}')
    
    for name in config.ALLOWED_TOKENS:
        responce = requests.get(
            url=f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?slug={name}&start=1&quoteCurrencyId=825&limit=100&category=spot&centerType=all&sort=cmc_rank_advanced&direction=desc&spotUntracked=true',
            headers=config.HEADER
        )
        if responce.ok:
            with open(f'data/tokenPairs/{name}.json', '+a') as file:
                json.dump(responce.json(), file)
        else:
            continue
    
    ARBITRAGES = format_arbitrages(process_file())



def process_file() -> list[dict]:  # sourcery skip: use-contextlib-suppress
    """
    эта функция обрабатывает файлы в папке data 
    и возвращает список отформатированых арбитражей

    пример: 
    returns:
            link = {
                'актив на бирже с высокой ценой': {
                    "имя биржи":        str,
                    "название пары":    str,
                    "цена":             float,
                    "ссылка":           str
                },
                'актив на бирже с низкой ценой': {
                    "имя биржи":        str,
                    "название пары":    str,
                    "цена":             float,
                    "ссылка":           str
                },
                'разница в процентах между высокой и низкой ценой': float,
                'время когда связка была найдена': str
            }
    """
    
    arbitrages = []

    for filename in os.listdir('data/tokenPairs'):
        try:
            with open(f"data/tokenPairs/{filename}", 'r', encoding='utf-8') as file:
                    data = json.load(file)['data']['marketPairs']
        
            """
            data выглядит примерно так:
                {
                    "rank": 1,
                    "exchangeId": 270,
                    "exchangeName": "Binance",
                    "exchangeSlug": "binance",
                    "exchangeNotice": "",
                    "outlierDetected": 0,
                    "priceExcluded": 0,
                    "volumeExcluded": 0,
                    "outlierDisp": 0,
                    "priceExDisp": 0,
                    "volExDisp": 0,
                    "marketId": 1108945,
                    "marketPair": "APT/USDT",
                    "category": "spot",
                    "marketUrl": "https://www.binance.com/en/trade/APT_USDT",
                    "marketScore": "0",
                    "marketReputation": 1,
                    "baseSymbol": "APT",
                    "baseCurrencyId": 21794,
                    "quoteSymbol": "USDT",
                    "quoteCurrencyId": 825,
                    "price": 8.51177556,
                    "volumeUsd": 56872257.90985084,
                    "effectiveLiquidity": 626.0,
                    "lastUpdated": "2025-01-24T17:44:16.000Z",
                    "quote": 8.51,
                    "volumeBase": 6681421.67705053,
                    "volumeQuote": 56858898.4717,
                    "feeType": "percentage",
                    "depthUsdNegativeTwo": 1126462.66587819,
                    "depthUsdPositiveTwo": 1084889.88748237,
                    "reservesAvailable": 1,
                    "porAuditStatus": 0,
                    "volumePercent": 23.313282544657,
                    "indexPrice": 0,
                    "isVerified": 1,
                    "quotes": [
                        {
                            "id": "2781",
                            "price": 8.51177556,
                            "volume24h": 56872257.90985084,
                            "depthPositiveTwo": 1084889.88748237,
                            "depthNegativeTwo": 1126462.66587819,
                            "indexPrice": 0.0
                        }
                    ],
                    "type": "cex",
                    "centerType": "cex",
                    "hideStarsMarket": 0
                }
            """
            new = {
                'max_pair': {
                    "exchangeName": None,
                    "marketPair": None,
                    "price": 0,
                    "marketUrl": ''
                },
                'min_pair': {
                    "exchangeName": None,
                    "marketPair": None,
                    "price": 0,
                    "marketUrl": ''
                },
                '%': None,
                'date': None
            }

            for pair in data:

                if pair['exchangeName'] not in config.ALLOWED_EXCHANGERS:
                    continue

                # if pair["exchangeName"] in ["HTX"]:
                #     continue

                try:
                    if pair["effectiveLiquidity"] < 1:
                        continue
                except KeyError:
                    continue
                
                if new['max_pair']['price'] < pair['price']:
                    new['max_pair'] = {
                        'exchangeName': pair['exchangeName'],
                        'marketPair': pair['marketPair'],
                        'price': pair['price'],
                        'marketUrl': pair['marketUrl'],
                        'volume24h': pair['quotes'][0]['volume24h']
                    }

                if new['min_pair']['price'] == 0:
                    new['min_pair']['price'] = pair['price']

                if new['min_pair']['price'] > pair['price']:
                    new['min_pair'] = {
                        'exchangeName': pair['exchangeName'],
                        'marketPair': pair['marketPair'],
                        'price': pair['price'],
                        'marketUrl': pair['marketUrl'],
                        'volume24h': pair['quotes'][0]['volume24h']
                    }

            difference = percentage_difference(
                new['max_pair']['price'],
                new['min_pair']['price']
            )

            if 2.5 <= difference <= 15:
                new['%'] = difference
                date = datetime.now(ZoneInfo('Europe/Moscow'))
                new['date'] = f"{date.day:0>{2}}.{date.month:0>{2}} | {date.hour}:{date.minute}:{date.second}"
                arbitrages.append(new)
            else:
                continue
        
        except Exception:
            pass

    return list(sorted(arbitrages, key=lambda x: x['%'], reverse=False))



def formatted_time() -> str:
    date = datetime.now(ZoneInfo('Europe/Moscow'))

    year = str(date.year)
    month = str(date.month).rjust(2, '0')
    day = str(date.day).rjust(2, '0')
    
    hour = str(date.hour).rjust(2, '0')
    minute = str(date.minute).rjust(2, '0')
    second = str(date.second).rjust(2, '0')
    
    date = f"{day}.{month}.{year}"
    time = f"{hour}:{minute}:{second}"
    
    time = f"{date} | {time}"

    return time



def format_volume(volume: float) -> str:
    if 0 <= volume < 1000:
        marker = '🔴 ликвидность пуста...'
    elif 1000 <= volume < 20_000:
        marker = '🟠 слабая ликвидность'
    elif 20_000 <= volume < 50_000:
        marker = '🟡 обьем в норме'
    else:
        marker = '🟢 хорошая ликвидность!'
    volume = f"{volume:.0f}"
    volume = list(volume[::-1])

    for index in range(3, len(volume)+2, 4):
        volume.insert(index, ' ')

    volume = list(reversed(volume))
    
    return f"{''.join(volume)} $\n│         {marker}"



def format_arbitrages(arbs: list[dict]) -> list[str]:
    result = []

    for item in arbs:
        if item['min_pair']['exchangeName'] is None or \
            item['min_pair']['marketPair'] is None or \
            item['min_pair']['price'] is None or \
            item['min_pair']['marketUrl'] is None or \
            item['max_pair']['exchangeName'] is None or \
            item['max_pair']['marketPair'] is None or \
            item['min_pair']['price'] is None or \
            item['min_pair']['marketUrl'] is None:
            continue
        
        minvolume24h = format_volume(volume=item['min_pair']['volume24h'])
        maxvolume24h = format_volume(volume=item['max_pair']['volume24h'])
        time = formatted_time()
        
        result.append(
f"""
┌─────────────
│ 🟢   <b>BUY</b>   🟢
│ - 🏦 <b>Биржа:</b> <i>{item['min_pair']['exchangeName']}</i>
│ - 🔗 <b>Пара:</b> <i>{item['min_pair']['marketPair']}</i>
│ - 💰 <b>Цена:</b> <i>{item['min_pair']['price']:.6f}</i>
│ - ⭕️ <b>Объем 24H:</b> {minvolume24h}
│ - 🌐 <b>Ссылка:</b> <i><a href="{item['min_pair']['marketUrl']}">{item['min_pair']['exchangeName']}</a></i>
│ 
│ ➖ - ➖ - ➖ - ➖ - ➖
│ 
│ 🔴   <b>SELL</b>   🔴
│ - 🏦 <b>Биржа:</b> <i>{item['max_pair']['exchangeName']}</i>
│ - 🔗 <b>Пара:</b> <i>{item['max_pair']['marketPair']}</i>
│ - 💰 <b>Цена:</b> <i>{item['max_pair']['price']:.6f}</i>
│ - ⭕️ <b>Объем 24H:</b> {maxvolume24h}
│ - 🌐 <b>Ссылка:</b> <i><a href="{item['max_pair']['marketUrl']}">{item['max_pair']['exchangeName']}</a></i>
│
│ -  ✅  <b>Profit:</b> {item['%']} %
│ -  📅  <b>{time}</b>
└─────────────
"""
        )
    
    return result
