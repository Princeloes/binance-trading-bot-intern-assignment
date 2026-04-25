import re

def validate_symbol(symbol: str) -> str:
    """
    Validates if the symbol looks like a valid pair (e.g. BTCUSDT).
    Kindly ensure it's alphanumeric and uppercase.
    """
    symbol = symbol.upper().strip()
    if not re.match(r"^[A-Z0-9]{4,15}$", symbol):
        raise ValueError(f"Invalid symbol format '{symbol}'. Please provide a valid pair like BTCUSDT.")
    return symbol

def validate_quantity(qty: float) -> float:
    """
    Quantity must be greater than zero.
    """
    if qty <= 0:
        raise ValueError("Quantity must be strictly positive (greater than 0). Kindly check the value.")
    return qty

def validate_price(price: float) -> float:
    """
    Price must be greater than zero.
    """
    if price <= 0:
        raise ValueError("Price must be strictly positive (greater than 0). Kindly check the value.")
    return price
