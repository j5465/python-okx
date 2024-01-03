from okx import Trade
from loadEnv import load_env_tuple
from okx.websocket.WsPublicAsync import WsPublicAsync
from okx.websocket.WsPprivateAsync import WsPrivateAsync


class SetUpApi:
    def __init__(self, isDemo="0"):
        self.api_key, self.api_secret_key, self.passphrase = load_env_tuple()
        print("SetUpApi api_key: " + self.api_key)
        self.tradeApi = Trade.TradeAPI(self.api_key, self.api_secret_key, self.passphrase, False, isDemo)

class SetUpWs:
    def __init__(self, url):
        api_key, api_secret_key, passphrase = load_env_tuple()
        self.ws = WsPrivateAsync(
            apiKey=api_key,
            passphrase=passphrase,
            secretKey=api_secret_key,
            url=url,
            useServerTime=False
        )