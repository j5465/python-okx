import time
import asyncio
import sys

from SetUpApi import SetUpApi
from okx.websocket.WsPublicAsync import WsPublicAsync
from okx import Account
from logger import get_my_logger    
import traceback


logUtil = get_my_logger("arb")

class SprdBookStatus:
    def __init__(self, ticker):
        self.ticker = ticker
        self.channel = "sprd-bbo-tbt"
        self.timeStamp = 0
    
# 数据格式
#   "arg": {
#     "channel": "sprd-books5",
#     "sprdId": "BTC-USDT_BTC-USDT-SWAP"
#   },
#   "data": [
#     {
#       "asks": [
#         ["111.06","55154","2"],],
#       "bids": [
#         ["111.05","57745","2"],],
#       "ts": "1670324386802"
#     }
#   ]
# asks和bids值数组举例说明： ["411.8", "10", "4"]
# - 411.8为深度价格
# - 10为此价格的数量 （单位为szCcy)
    
    def updateSprdBooks(self, message):
        arg = message["arg"]
        if arg["channel"] != self.channel or arg["sprdId"] != self.ticker:
            return
        data = message["data"]

        self.bidsPrice = data["bids"][0]
        self.bidsAmount = data["bids"][1]

        self.asksPrice = data["asks"][0]
        self.asksAmount = data["asks"][1]

        self.timeStamp = data["ts"]

    def TimeStampChangedWithPrice(self):
        return time.time() - self.timeStamp


class FundingRateArbitrageBot(SetUpApi):
    
    def __init__(self):
        super().__init__()
        self.AccountAPI = Account.AccountAPI(self.api_key, self.api_secret_key, self.passphrase, use_server_time=False, flag='0')
        url = "wss://wspap.okx.com:8443/ws/v5/business"
        self.ws = WsPublicAsync(url=url)
        subChannels = []
        TickersPriceLimit = {}
        self.sprdBookStatus = None

    async def startWs(self):
        await self.ws.start()

    def BuildMarketTradeOrder(self, instId, tdMode, side, sz, tgtCcy=None):
        order = {
            "instId": instId,
            "tdMode": tdMode,
            "side": side,
            "ordType": "market",
            "sz": sz
        }
        # 只有币币交易需要填tgtCcy，使用交易货币计数
        if tgtCcy:
            order['tgtCcy'] = tgtCcy
        return order
    
    def place_multiple_order(self, orders):
        orders_res = self.tradeApi.place_multiple_orders(orders)

        logUtil.debug("FundingRateArbitrageBot place_multiple_order result: " + str(orders_res))
        return orders_res
    
    def control_risk(self):
        try:        
            res = self.AccountAPI.get_positions("SWAP", "NOT-USDT-SWAP")
            logUtil.debug(res)

            if res['code'] == '0':
                if len(res['data']) == 1:
                    notionalUsd = float(res['data'][0]['notionalUsd'])
                    if notionalUsd > 5300:
                        buy_args = "trade buy NMR-USDT 20 NMR-USDT-SWAP 201".split()
                        op_trade(buy_args)
        except Exception as e:
            logUtil.error(traceback.format_exc())
            self.AccountAPI = Account.AccountAPI(self.api_key, self.api_secret_key, self.passphrase, use_server_time=False, flag='0')

            

    # 腿交易sprd-bbo-tbt, sprd-books5
    async def subscribeSprdBooks(self, sprdId):
        arg1 =   {
            "channel": "sprd-bbo-tbt",
            "sprdId": sprdId
        }
        self.sprdBookStatus = SprdBookStatus(sprdId)
        await self.ws.subscribe([arg1], lambda message : self.sprdBookStatus.updateSprdBooks(message))

    def getSprdBookStatus(self):
        return self.sprdBookStatus


    def updateTickersPriceLimit(self, message):
        pass

    # 限价频道price-limit
    async def subscribeTickerPriceLimit(self, ticker):
        arg1 = {"channel": "price-limit", "instId": ticker}
        if arg1 in self.subChannels:
            logUtil.debug("已经订阅price-limit, tiker:" + ticker)
            return
        self.subChannels.append(arg1)
        await self.ws.subscribe([arg1], lambda message : self.updateTickersPriceLimit(message))

    


def publicCallback(message):
    logUtil.debug("publicCallback", message)

def op_trade(input_args):
    derivatives_side, margin_instId, margin_sz, derivatives_instId, derivatives_sz = input_args[1:]

    margin_order = bot.BuildMarketTradeOrder(margin_instId, "cross", "sell" if derivatives_side == "buy" else "buy", margin_sz, "base_ccy")
    derivatives_order = bot.BuildMarketTradeOrder(derivatives_instId, "cross", derivatives_side, derivatives_sz)
    print(str(derivatives_order))

    hedge_orders = [margin_order, derivatives_order]
    bot.place_multiple_order(hedge_orders)

    logUtil.debug("shuru: " + str(derivatives_order) + " " + str(margin_order))



def op_sprd_status():
    logUtil.debug(bot.getSprdBookStatus().TimeStampChangedWithPrice())



async def main():
    # 获取命令行参数，跳过脚本名称
    input_args = sys.argv[1:]
    
    if not input_args:
        print("请提供参数")
        return
        
    op_type = input_args[0]
    if op_type == "trade":
        op_trade(input_args=input_args)
    elif op_type == "sub_sprd":
        await bot.startWs()
        sprdId = input_args[1:]
        await bot.subscribeSprdBooks(sprdId)
    elif op_type == "sprd_status":
        op_sprd_status()
    elif op_type == "risk_monitor":
        while True:
            bot.control_risk()
            time.sleep(5)

if __name__ == '__main__':
    bot = FundingRateArbitrageBot()
    asyncio.run(main())

