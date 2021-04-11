import requests
from random import randint


class ProxyCoinSwitch:
    def __init__(self):
        self.api_key = 'jKl133doyq4H34UfVJBk86le2v4t6ycex1XGZIv8'
        self.debug = True

    def _authenticate(self):
        ip = ".".join(map(str, (randint(0, 255)
                                for _ in range(4))))
        return {"x-user-ip": ip, "x-api-key": self.api_key}

    def list_currencies(self):
        url = "https://api.coinswitch.co/v2/coins"
        response = requests.get(url, headers=self._authenticate())
        if self.debug:
            print(response.text)
        return response.text

    def list_pairs(self, deposit: str = 'btc', destination: str = None):
        url = "https://api.coinswitch.co/v2/pairs"
        payload = {"depositCoin": f"{deposit}", "destinationCoin": {destination}}
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, json=payload, headers=headers.update(self._authenticate()))
        if self.debug:
            print(response.text)
        return response.text

    def quote(self, deposit: str = 'btc', destination: str = 'eth', qty: float = 1000.00):
        url = "https://api.coinswitch.co/v2/rate"

        payload = {
            "depositCoin": deposit,
            "destinationCoin": destination,
            "depositCoinAmount": qty
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers.update(self._authenticate()))

        if self.debug:
            print(response.text)
        return response.text

    def order(self, deposit_coin, destination_coin, deposit_qty: float = 0.0, destination_qty: float = 0.0,
              destination_address: str = None, refund_address: str = None):
        url = "https://api.coinswitch.co/v2/order"
        if not deposit_qty or destination_qty:
            print('Must supply either a deposit or destination qty.')
            return False
        if not destination_address and refund_address:
            print('Must supply both destination and refund address')
            return False

        payload = {
            "depositCoin": deposit_coin,
            "destinationCoin": destination_coin,
            "depositCoinAmount": deposit_qty,
            "destinationCoinAmount": destination_qty,
            "destinationAddress": destination_address,
            "refundAddress": refund_address
        }
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=payload, headers=headers.update(self._authenticate()))

        if self.debug:
            print(response.text)
        return response.text

    def status(self, order_id: str = None):
        headers = self._authenticate()
        if not order_id:
            print('Must supply order id')
            return False

        url = f"https://api.coinswitch.co/v2/order{order_id}"

        response = requests.get(url, headers=headers)
        if self.debug:
            print(response.text)
        return response.text

    def exchange_history(self):
        url = "https://api.coinswitch.co/v2/orders"

        response = requests.get(url, headers=self._authenticate())
        if self.debug:
            print(response.text)
        return response.text
