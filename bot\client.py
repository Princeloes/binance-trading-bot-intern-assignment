import time
import hmac
import hashlib
import requests
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from bot.logging_config import logger

class BinanceTestnetClient:
    """
    A simplified client for Binance Futures Testnet.
    We are using direct REST calls to showcase the structure instead of heavy libraries.
    Kindly check your API keys are correct before doing the needful.
    """
    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })
        logger.debug("BinanceTestnetClient initialized.")

    def _generate_signature(self, query_string: str) -> str:
        """
        Kindly generate HMAC SHA256 signature for the request.
        """
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _dispatch_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Dispatches the request to Binance testnet.
        Handles errors and logging. Please revert back if there are connection issues.
        """
        if params is None:
            params = {}

        # Add timestamp, required for signed endpoints
        params['timestamp'] = int(time.time() * 1000)
        
        # Prepare query string
        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        
        # Construct final URL
        url = f"{self.BASE_URL}{endpoint}?{query_string}&signature={signature}"
        
        logger.debug(f"Dispatching {method} request to {endpoint} with params: {params}")

        try:
            response = self.session.request(method, url)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            logger.debug(f"Response received: {data}")
            return data
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP Error occurred: {err}")
            # Try to get Binance specific error message
            try:
                error_data = response.json()
                logger.error(f"Binance Error details: {error_data}")
            except Exception:
                pass
            raise
        except requests.exceptions.ConnectionError as err:
            logger.error(f"Network Connection Error: kindly check your internet. Details: {err}")
            raise
        except Exception as err:
            logger.error(f"An unexpected error occurred: {err}")
            raise

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
        """
        Places an order on the testnet.
        """
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        
        if order_type == "LIMIT":
            if price is None:
                raise ValueError("Price is compulsory for LIMIT orders, kindly provide it.")
            params["price"] = price
            params["timeInForce"] = "GTC" # Good Till Cancel

        logger.info(f"Placing {order_type} {side} order for {quantity} {symbol}...")
        return self._dispatch_request("POST", endpoint, params)

