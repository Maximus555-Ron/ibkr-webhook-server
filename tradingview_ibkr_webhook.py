import os
from flask import Flask, request
from ib_insync import *

app = Flask(__name__)

# === Connect to TWS / IB Gateway ===
ib = IB()
try:
    ib.connect('127.0.0.1', 7497, clientId=1)
except Exception as e:
    print(f"🚨 API connection failed: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    # Extract fields
    symbol = data.get('symbol')
    action = data.get('signal').upper()
    price = float(data.get('price'))
    quantity = 10

    print(f"📡 Signal received: {action} {symbol} @ {price}")

    contract = Stock(symbol, 'SMART', 'USD')
    order = LimitOrder(action, quantity, price)

    try:
        ib.qualifyContracts(contract)              # ✅ Fully synchronous
        trade = ib.placeOrder(contract, order)     # ✅ Fully synchronous
        ib.sleep(1)
        print(f"✅ Order placed: {action} {symbol} @ {price}")
    except Exception as e:
        print(f"🚨 Order error: {e}")

    return f"Executed {action} {symbol} @ {price}", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)