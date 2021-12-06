import socketio
import requests

TOKEN = "<TOKEN>"
tgUrl = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
tauUsdPriceApi = "https://rocketswap.exchange:2053/api/tau_last_price"
chat_id = <CHAT_ID>
parse_mode = "Markdown"
sio = socketio.Client(logger=True)

@sio.event
def connect():
    print("connected!")
    
@sio.on("trade_update:global")
def update_trade(trade_data):
    tauPriceUsd = float(requests.get(tauUsdPriceApi).json()["value"])
    type = trade_data["type"]
    amount = float(trade_data["amount"])
    token = trade_data["token_symbol"]
    amountTxt = '%.4f'%(amount)
    price = float(trade_data["price"])
    priceTxt = '%.4f'%(price)
    tokenPriceUsd = price * tauPriceUsd
    tokenPriceUsdTxt = '%.2f'%(tokenPriceUsd)
    tokenAmtUsd = amount *  tokenPriceUsd
    tokenAmtUsdTxt = '%.2f'%(tokenAmtUsd)
    hash = trade_data["hash"]
    
    if type == "buy":
        buy_text1 = f"🟢 #{token}\nBought `{amountTxt}` *{token}* *(${tokenAmtUsdTxt})* on [RocketSwap](https://rocketswap.exchange/#/swap/)🚀\n\n@ *Price* `{priceTxt}` *TAU* *($~{tokenPriceUsdTxt})*\n>>[View txn on Explorer](https://mainnet.lamden.io/transactions/{hash})<<"
        buy_text2 = f"🟢🟢 #{token}\nBought `{amountTxt}` *{token}* *(${tokenAmtUsdTxt})* on [RocketSwap](https://rocketswap.exchange/#/swap/)🚀\n\n@ *Price* `{priceTxt}` *TAU* *($~{tokenPriceUsdTxt})*\n>>[View txn on Explorer](https://mainnet.lamden.io/transactions/{hash})<<"
        buy_text3 = f"🟢🟢🟢 #{token}\nBought `{amountTxt}` *{token}* *(${tokenAmtUsdTxt})* on [RocketSwap](https://rocketswap.exchange/#/swap/)🚀\n\n@ *Price* `{priceTxt}` *TAU* *($~{tokenPriceUsdTxt})*\n>>[View txn on Explorer](https://mainnet.lamden.io/transactions/{hash})<<"
        if tokenAmtUsd >= 100 and tokenAmtUsd <= 399:
            data = {
                "chat_id": chat_id,
                "parse_mode": parse_mode,
                "text": buy_text1
            }
            requests.post(tgUrl, data)
        if tokenAmtUsd >= 400 and tokenAmtUsd <= 899:
            data = {
                "chat_id": chat_id,
                "parse_mode": parse_mode,
                "text": buy_text2
            }
            requests.post(tgUrl, data)
        if tokenAmtUsd >= 900:
            data = {
                "chat_id": chat_id,
                "parse_mode": parse_mode,
                "text": buy_text3
            }
            requests.post(tgUrl, data) 
    else:
        sold_text1 = f"🔴 #{token}\nSold `{amountTxt}` *{token}* *(${tokenAmtUsdTxt})* on [RocketSwap](https://rocketswap.exchange/#/swap/)🚀\n\n@ *Price* `{priceTxt}` *TAU* *($~{tokenPriceUsdTxt})*\n>>[View txn on Explorer](https://mainnet.lamden.io/transactions/{hash})<<"
        sold_text2 = f"🔴🔴 #{token}\nSold `{amountTxt}` *{token}* *(${tokenAmtUsdTxt})* on [RocketSwap](https://rocketswap.exchange/#/swap/)🚀\n\n@ *Price* `{priceTxt}` *TAU* *($~{tokenPriceUsdTxt})*\n>>[View txn on Explorer](https://mainnet.lamden.io/transactions/{hash})<<"
        sold_text3 = f"🔴🔴🔴 #{token}\nSold `{amountTxt}` *{token}* *(${tokenAmtUsdTxt})* on [RocketSwap](https://rocketswap.exchange/#/swap/)🚀\n\n@ *Price* `{priceTxt}` *TAU* *($~{tokenPriceUsdTxt})*\n>>[View txn on Explorer](https://mainnet.lamden.io/transactions/{hash})<<"
        if tokenAmtUsd >= 100 and tokenAmtUsd <= 399:
            data = {
                "chat_id": chat_id,
                "parse_mode": parse_mode,
                "text": sold_text1
            }
            requests.post(tgUrl, data)
        if tokenAmtUsd >= 400 and tokenAmtUsd <= 899:
            data = {
                "chat_id": chat_id,
                "parse_mode": parse_mode,
                "text": sold_text2
            }
            requests.post(tgUrl, data)
        if tokenAmtUsd >= 900:
            data = {
                "chat_id": chat_id,
                "parse_mode": parse_mode,
                "text": sold_text3
            }
            requests.post(tgUrl, data)
@sio.event
def connect_error(err):
    print(err)
    
@sio.event
def disconnect():
    print("disconnected!")
    
sio.connect("https://rocketswap.exchange:2053")
sio.wait()
