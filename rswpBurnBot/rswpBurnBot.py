import requests
import time
from datetime import datetime

TOKEN = "<TOKEN>"
tgUrl = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
burnApiUrl = "<BLOCK_SERVICE_ENDPOINT>"
tauUsdPriceApi = "https://rocketswap.exchange:2053/api/tau_last_price"
rswpPriceApi = "https://rocketswap.exchange:2053/api/token/con_rswp_lst001"
chat_id = <CHAT_ID1>
chat_id2 =  <CHAT_ID2>
parse_mode = "Markdown"

inital_burn = float(requests.get(burnApiUrl).json()["con_rswp_lst001"]["balances"]["burn"]["__fixed__"])
current_burn = inital_burn
current_24burn = current_burn
current_time = datetime.utcnow().strftime("%H:%M")
current_24time = current_time
def update():
    global current_burn
    global current_24burn
    global current_time
    global current_24time
    count = 0
    while True:
        time.sleep(10800)# 10800
         burned = float(requests.get(burnApiUrl).json()["con_rswp_lst001"]["balances"]["burn"]["__fixed__"])
        tauPriceUsd = float(requests.get(tauUsdPriceApi).json()["value"])
        rswpPrice = float(requests.get(rswpPriceApi).json()["lp_info"]["price"])
        last_burn = burned - current_burn
        rswpPriceUsd = '%.2f'%(last_burn * rswpPrice * tauPriceUsd)
        current_burn = burned
        last_time = current_time

        text = f"🔥*BURNED*🔥 `{'%.4f'%(last_burn)}` `RSWP` *($~{rswpPriceUsd})* _since {last_time}_ UTC⏱"
        data = {
            "chat_id": chat_id,
            "parse_mode": parse_mode,
            "text": text
        }

        data2 = {
            "chat_id": chat_id2,
            "parse_mode": parse_mode,
            "text": text
        }


        requests.post(tgUrl, data)
        requests.post(tgUrl, data2)
        current_time = datetime.utcnow().strftime("%H:%M")
        count += 1
        if count == 8:
          last_24burn = burned - current_24burn
          last_24time = current_24time
          rswpPriceUsd24 = '%.2f'%(last_24burn * rswpPrice * tauPriceUsd)
          count = 0

          text24 = f"🔥*BURNED*🔥 `{'%.4f'%(last_24burn)}` `RSWP` *($~{rswpPriceUsd24})* _in 24hrs_ UTC⏱"
          data24 = {
              "chat_id": chat_id,
              "parse_mode": parse_mode,
              "text": text24
          }

          data224 = {
              "chat_id": chat_id2,
              "parse_mode": parse_mode,
              "text": text24
          }


          requests.post(tgUrl, data24)
          requests.post(tgUrl, data224)
          current_24time = current_time
          
update()








