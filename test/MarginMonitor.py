import time
import asyncio
import threading

from okx.websocket.WsPublic import WsPublic
from SetUpApi import SetUpWs
from okx.websocket.WsPublicAsync import WsPublicAsync
from okx.websocket.WsPprivateAsync import WsPrivateAsync

def cb1(message):
    print("privateCallback", message) 

class MarginMonitor(SetUpWs):
    def __init__(self):
        # super().__init__("wss://ws.okx.com:8443/ws/v5/private")
        pass
    def privateCallback(self, message):

        print("privateCallback", message) 



    async def start(self):
        url = "wss://ws.okx.com:8443/ws/v5/private"
        ws = WsPrivateAsync(
            apiKey="60450202-8310-4136-a697-cccfb34e2697",
            passphrase="zxshhhh123ZXC...",
            secretKey="9A7203FFD36FB17FEE62CA2BB5571C43",
            url=url,
            useServerTime=False
        )
        await ws.start()
        arg1 = {"channel": "balance_and_position"}
        # arg3 = {"channel": "positions",
        #         "instType": "MARGIN",
        #         "instId": "SATS-USDT"
        #         }
        print("abc")
        await ws.subscribe([arg1], callback=cb1)

        # await self.ws.subscribe([arg3], callback=lambda x : self.privateCallback(x))

        ticker = 0
        while(True):
            print("in start")
            if ticker % 10 == 0:
                pass
            await asyncio.sleep(1)
            ticker += 1




def main():
    monitor = MarginMonitor()
    asyncio.run(monitor.start())



if __name__ == '__main__':
    main()