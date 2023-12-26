import time

from okx.websocket.WsPublic import WsPublic
from SetUpApi import SetUpApi

class FundingRateArbitrageBot(SetUpApi):
    
    def __init__(self):
        super().__init__()

    def BuildeMarketTradeOrder(self, instId, tdMode, side, sz, tgtCcy=None):
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
        print("FundingRateArbitrageBot place_multiple_order result: " + str(self.tradeApi.place_multiple_orders(orders)))


    


def publicCallback(message):
    print("publicCallback", message)


if __name__ == '__main__':
    bot = FundingRateArbitrageBot()
    while True:
        input_data = input()

        input_args = input_data.split()
        if not input_data:
            # todo 请求下两边的价格, 看一下合约溢价
            break
        # switch()
        derivatives_side, margin_instId, margin_sz, derivatives_instId, derivatives_sz = input_args[0:]
        margin_side = ""
        if derivatives_side == "buy":
            margin_side = "sell"
        elif derivatives_side == "sell":
            margin_side = "buy"
        else:
            break
        hedge_orders = [bot.BuildeMarketTradeOrder(margin_instId, "cross", margin_side, margin_sz, "base_ccy"),
                        bot.BuildeMarketTradeOrder(derivatives_instId, "cross", derivatives_side, derivatives_sz)
                        ]

        bot.place_multiple_order(hedge_orders)

        print("shuru: " + str(hedge_orders))

    #url = "wss://wspri.coinall.ltd:8443/ws/v5/ipublic?brokerId=9999"
    # url = "wss://wspap.okex.com:8443/ws/v5/public"
    # ws = WsPublic(url=url)
    # ws.start()
    # args = []
    # arg1 = {"channel": "tickers", "instId": "SATS-USDT"}
    # arg2 = {"channel": "tickers", "instId": "SATS-USDT-SWAP"}
    # args.append(arg1)
    # args.append(arg2)

    # ws.subscribe(args, publicCallback)
    # time.sleep(10)
    # print("-----------------------------------------unsubscribe all--------------------------------------------")
    # args3 = [arg1, arg2]
    # ws.unsubscribe(args3, publicCallback)
