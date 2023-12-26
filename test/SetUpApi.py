from okx import Trade
from loadEnv import load_env_tuple


class SetUpApi:
    def __init__(self, isDemo="0"):
        api_key, api_secret_key, passphrase = load_env_tuple()
        print("SetUpApi api_key: " + api_key)
        self.tradeApi = Trade.TradeAPI(api_key, api_secret_key, passphrase, False, isDemo)
