import asyncio

from okx.websocket.WsPprivateAsync import WsPrivateAsync


def privateCallback(message):
    print("privateCallback", message)


async def main():
    url = "wss://ws.okx.com:8443/ws/v5/private"
    ws = WsPrivateAsync(
        apiKey="60450202-8310-4136-a697-cccfb34e2697",
        passphrase="zxshhhh123ZXC...",
        secretKey="9A7203FFD36FB17FEE62CA2BB5571C43",
        url=url,
        useServerTime=False
    )
    await ws.start()
    args = []
    # arg1 = {"channel": "account", "instType": "BTC"}
    # arg2 = {"channel": "orders", "instType": "ANY"}
    arg3 = {"channel": "balance_and_position"}
    # args.append(arg1)
    # args.append(arg2)
    args.append(arg3)
    await ws.subscribe(args, callback=privateCallback)
    await asyncio.sleep(30)
    print("-----------------------------------------unsubscribe--------------------------------------------")
    # args2 = [arg2]
    # await ws.unsubscribe(args2, callback=privateCallback)
    # await asyncio.sleep(30)
    # print("-----------------------------------------unsubscribe all--------------------------------------------")
    # args3 = [arg1, arg3]
    # await ws.unsubscribe(args3, callback=privateCallback)


if __name__ == '__main__':
    asyncio.run(main())
