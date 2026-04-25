from typing import Optional, Dict, Any
from bot.client import BinanceTestnetClient
from bot.logging_config import logger

def execute_order(
    api_key: str,
    api_secret: str,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Wrapper function to execute the order.
    Kindly initializes the client and places the order, then reverts back with the response.
    """
    try:
        client = BinanceTestnetClient(api_key, api_secret)
        
        logger.info(f"Initiating order request for {symbol}. Side: {side}, Type: {order_type}")
        
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        logger.info(f"Order successfully placed. Order ID: {response.get('orderId')}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to execute order: {str(e)}")
        raise
