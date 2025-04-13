import os
from flask import Flask, request
from ib_insync import *

app = Flask(__name__)

# === Connect to TWS or IB Gateway ===
ib = IB()
try:
    ib.connect('127.0.0.1', 7497, clientId=1)
except Exception as e:
    print(f"API connection failed: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Extract fields from TradingView
    symbol = data.get('symbol')
    action = data.get('signal').upper()
    price = float(data.get('price'))
    quantity = 10  # Default trade size

    print(f"📡 Received signal: {action} {symbol} at {price}")

    contract = Stock(symbol, 'SMART', 'USD')
    order = LimitOrder(action, quantity, price)

    try:
        ib.run(ib.qualifyContractsAsync(contract))  # FIXED ✅
        ib.run(ib.placeOrder(contract, order))      # FIXED ✅
        ib.sleep(1)  # Let it process
        print(f"✅ Placed {action} order for {symbol} at {price}")
    except Exception as e:
        print(f"🚨 Order error: {e}")

    return f"Executed {action} {symbol} @ {price}", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)