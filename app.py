from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CHANGE_THIS_TO_A_SECRET_VALUE'  # Change this to a secret value

# HTML template with inline CSS and JavaScript
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stock Market</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background-color: #fff;
            border: 1px solid #ddd;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        .stock-symbol {
            font-size: 24px;
            font-weight: bold;
        }
        .stock-price {
            font-size: 18px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Stock Market</h1>
        <form>
            <input type="text" id="stock-symbol" placeholder="Enter stock symbol">
            <button id="get-stock-btn">Get Stock</button>
        </form>
        <div id="stock-info"></div>
    </div>
    <script>
        const getStockBtn = document.getElementById('get-stock-btn');
        const stockSymbolInput = document.getElementById('stock-symbol');
        const stockInfoDiv = document.getElementById('stock-info');

        getStockBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const stockSymbol = stockSymbolInput.value.trim();
            if (stockSymbol) {
                fetch(`/?stock_symbol=${stockSymbol}`)
                    .then((res) => res.json())
                    .then((data) => {
                        if (data.error) {
                            stockInfoDiv.innerText = data.error;
                        } else {
                            stockInfoDiv.innerHTML = `
                                <p class="stock-symbol">${data.symbol}</p>
                                <p class="stock-price">Price: $${data.price}</p>
                            `;
                        }
                    })
                    .catch((err) => console.error(err));
            }
        });
    </script>
</body>
</html>
'''

# API endpoint to get stock info
@app.route('/', methods=['GET'])
def get_stock_info():
    stock_symbol = request.args.get('stock_symbol')
    if stock_symbol:
        try:
            stock_data = yf.Ticker(stock_symbol)
            stock_info = stock_data.info
            if 'currentPrice' in stock_info:
                stock_price = stock_info['currentPrice']
                return jsonify({'symbol': stock_symbol, 'price': stock_price})
            else:
                return jsonify({'error': 'Failed to retrieve stock price'})
        except Exception as e:
            return jsonify({'error': str(e)})
    return html_template

if __name__ == '__main__':
    app.run(debug=True)