# Binance Futures Testnet Trading Bot

Hello! This is a simplified trading bot built for the Binance Futures Testnet (USDT-M), created as an assignment for the Python Developer Intern role at Primetrade.ai.

## Setup Steps

Kindly follow the below steps to setup the project on your local system:

1. **Clone the repository or extract the zip folder.**
2. **Create a virtual environment (optional but recommended to do the needful):**
   ```bash
   python -m venv venv
   # On Windows
   venv\\Scripts\\activate
   # On Linux/Mac
   source venv/bin/activate
   ```
3. **Install the requirements:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up API Credentials:**
   - Register on [Binance Futures Testnet](https://testnet.binancefuture.com/)
   - Generate your API Key and Secret Key.
   - Rename the `.env.example` file to `.env`.
   - Paste your keys inside the `.env` file. Kindly ensure you don't share this file with anyone.

## How to Run Examples

This bot comes with an interactive CLI. You can use it directly or via interactive prompts.

### Example 1: Placing a MARKET order
```bash
python cli.py trade --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Example 2: Placing a LIMIT order
```bash
python cli.py trade --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 95000.50
```

### Interactive Mode
If you miss any arguments, the bot will gently prompt you to provide them:
```bash
python cli.py trade
```

## Features Implemented
- **Direct REST Implementation**: No heavy `python-binance` dependency. Implemented custom HMAC SHA256 signing for maximum control.
- **Enhanced CLI UX (Bonus)**: Used `Typer` and `Rich` to provide menus, prompts, validation messages, and colored output.
- **Proper Logging**: Logs API requests, responses, and errors to `bot.log` in a clean format.
- **Robust Error Handling**: Catches network issues, validation errors, and Binance API errors gracefully.

## Assumptions
- It is assumed that the user has sufficient margin/balance in their Binance Futures Testnet account before placing an order.
- It is assumed the user will provide valid precision for quantity and price as per Binance rules (e.g., BTCUSDT qty usually goes up to 3 decimals).
- The `timeInForce` for LIMIT orders is hardcoded to `GTC` (Good Till Cancel) as per standard practice.

Kindly revert back if you face any doubts regarding the run process.
