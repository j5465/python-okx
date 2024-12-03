import time
import traceback
from okx import Account
from logger import get_my_logger
from SetUpApi import SetUpApi
from flask import Flask, jsonify, request
from zijinfei import FundingRateArbitrageBot

logUtil = get_my_logger("risk_control")
app = Flask(__name__)

class RiskController(SetUpApi):
    def __init__(self):
        super().__init__()
        self.bot = FundingRateArbitrageBot()
        self.position_info = {"timestamp": "", "notionalUsd": 0}

    def op_trade(self, input_args):
        derivatives_side, margin_instId, margin_sz, derivatives_instId, derivatives_sz = input_args[1:]

        margin_order = self.bot.BuildMarketTradeOrder(margin_instId, "cross", "sell" if derivatives_side == "buy" else "buy", margin_sz, "base_ccy")
        derivatives_order = self.bot.BuildMarketTradeOrder(derivatives_instId, "cross", derivatives_side, derivatives_sz)
        print(str(derivatives_order))

        hedge_orders = [margin_order, derivatives_order]
        self.bot.place_multiple_order(hedge_orders)

        logUtil.debug("shuru: " + str(derivatives_order) + " " + str(margin_order))
    def control_risk(self):
        try:        
            res = self.bot.AccountAPI.get_positions("SWAP", "NMR-USDT-SWAP")
            logUtil.debug(res)

            if res['code'] == '0':
                if len(res['data']) == 1:
                    notionalUsd = float(res['data'][0]['notionalUsd'])
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    logUtil.debug(f"时间: {current_time}, notionalUsd: {int(notionalUsd)}")
                    self.position_info = {
                        "timestamp": current_time,
                        "notionalUsd": notionalUsd
                    }

                    if notionalUsd > 530:
                        buy_args = "trade buy NMR-USDT 20 NMR-USDT-SWAP 201".split()

                        self.op_trade(buy_args)
        except Exception as e:
            logUtil.error(traceback.format_exc())
            self.bot.AccountAPI = Account.AccountAPI(
                self.api_key, 
                self.api_secret_key, 
                self.passphrase, 
                use_server_time=False, 
                flag='0'
            )

risk_controller = RiskController()

@app.route('/position', methods=['GET'])
def get_position():
    key = request.args.get('key')
    if key != 'SDFNIUNsdfuinb87678575':
        return jsonify({"error": "Invalid key"}), 403
    return jsonify(risk_controller.position_info)

def run_risk_control():
    while True:
        risk_controller.control_risk()
        time.sleep(5)

if __name__ == "__main__":
    import threading
    try:
        print("开始启动风险控制线程")
        # 启动风险控制线程
        risk_thread = threading.Thread(target=run_risk_control)
        risk_thread.daemon = True
        risk_thread.start()
        print("风险控制线程已启动")
        # 添加日志，确认服务启动
        logUtil.info("正在启动Flask服务，端口8000...")
        
        # 启动Flask服务
        app.run(host='0.0.0.0', port=8320, debug=False)  # 添加debug模式便于排查问题
    except Exception as e:
        logUtil.error(f"服务启动失败: {str(e)}")
        logUtil.error(traceback.format_exc())