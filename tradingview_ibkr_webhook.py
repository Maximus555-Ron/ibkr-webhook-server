import os
from flask import Flask, request
from ib_insync import *

app = Flask(__name__)

# === Connect to Trader Workstation (TWS) or IB Gateway ===
ib = IB()
try:
    ib.connect('127.0.0.1', 7497, clientId=1)  # For paper trading
except Exception as e:
    print(f"API connection failed: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Extract fields from TradingView
    symbol = data.get('symbol')
    action = data.get('signal').upper()
    price = float(data.get('price'))
    quantity = 10  # Set your preferred trade size

    print(f"📡 Received signal: {action} {symbol} at {price}")

    # Prepare order
    contract = Stock(symbol, 'SMART', 'USD')
    order = LimitOrder(action, quantity, price)

    try:
        ib.qualifyContracts(contract)
        trade = ib.placeOrder(contract, order)
        ib.sleep(1)  # Allow time for IBKR to process the order
        print(f"✅ Placed {action} order for {symbol} at {price}")
    except Exception as e:
        print(f"🚨 Order error: {e}")

    return f"Executed {action} {symbol} @ {price}", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)