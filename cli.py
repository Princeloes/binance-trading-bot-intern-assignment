import os
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from dotenv import load_dotenv

from bot.validators import validate_symbol, validate_quantity, validate_price
from bot.orders import execute_order
from bot.logging_config import logger

# Load environment variables (API credentials)
load_dotenv()

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI. Kindly use the 'trade' command to do the needful.")
console = Console()

@app.command()
def trade(
    symbol: str = typer.Option(..., prompt="Enter trading symbol (e.g., BTCUSDT)", help="Trading pair symbol"),
    side: str = typer.Option(..., prompt="Enter side (BUY/SELL)", help="Order side"),
    order_type: str = typer.Option(..., prompt="Enter order type (MARKET/LIMIT)", help="Order type"),
    quantity: float = typer.Option(..., prompt="Enter quantity", help="Order quantity"),
    price: float = typer.Option(None, help="Price for LIMIT orders")
):
    """
    Places an order on Binance Futures Testnet.
    """
    console.print("[bold blue]Starting trading bot...[/bold blue]")
    
    # Validation step
    try:
        side = side.upper().strip()
        order_type = order_type.upper().strip()
        
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be strictly BUY or SELL.")
            
        if order_type not in ["MARKET", "LIMIT"]:
            raise ValueError("Order type must be strictly MARKET or LIMIT.")
            
        symbol = validate_symbol(symbol)
        quantity = validate_quantity(quantity)
        
        if order_type == "LIMIT":
            if price is None:
                price = typer.prompt("Price is required for LIMIT orders. Kindly enter price", type=float)
            price = validate_price(price)
            
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)
        
    # Credentials check
    api_key = os.getenv("BINANCE_TESTNET_API_KEY")
    api_secret = os.getenv("BINANCE_TESTNET_API_SECRET")
    
    if not api_key or not api_secret or api_key == "your_api_key_here":
        msg = "API credentials not found in .env file. Kindly check the .env file and do the needful."
        logger.error(msg)
        console.print(f"[bold red]{msg}[/bold red]")
        raise typer.Exit(1)

    # Order Request Summary
    summary_table = Table(title="Order Request Summary")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="magenta")
    summary_table.add_row("Symbol", symbol)
    summary_table.add_row("Side", side)
    summary_table.add_row("Type", order_type)
    summary_table.add_row("Quantity", str(quantity))
    if order_type == "LIMIT":
        summary_table.add_row("Price", str(price))
        
    console.print(summary_table)
    
    confirm = typer.confirm("Do you want to proceed and place this order?")
    if not confirm:
        console.print("[yellow]Order placement cancelled. Reverting back.[/yellow]")
        raise typer.Exit()
        
    # Execution
    try:
        response = execute_order(
            api_key=api_key,
            api_secret=api_secret,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Output Response Details
        console.print("\n[bold green]Success! Order placed successfully.[/bold green]")
        
        res_table = Table(title="Order Response Details")
        res_table.add_column("Field", style="cyan")
        res_table.add_column("Value", style="green")
        
        # Safely get values from response
        res_table.add_row("Order ID", str(response.get("orderId", "N/A")))
        res_table.add_row("Status", str(response.get("status", "N/A")))
        res_table.add_row("Executed Qty", str(response.get("executedQty", "N/A")))
        res_table.add_row("Average Price", str(response.get("avgPrice", "N/A")))
        
        console.print(res_table)
        
    except Exception as e:
        console.print(f"\n[bold red]Failed to place order![/bold red]")
        console.print(f"Error details: {e}")
        console.print("Kindly check the bot.log file for more information.")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
