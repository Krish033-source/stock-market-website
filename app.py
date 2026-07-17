# Runtime dependencies:
# - Flask
# - yfinance
# - matplotlib
# - pandas

from flask import Flask, render_template_string
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a proper secret key

# Define the top 10 Indian stocks
indian_stocks = ['INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'LT.NS', 'AXISBANK.NS', 
                 'TATAMOTORS.NS', 'HCLTECH.NS', 'BHARTIARTL.NS', 'ASIANPAINT.NS', 'TCS.NS']

# Define the HTML template
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Indian Stocks</title>
    <style>
        body {
            background-color: #2f2f2f;
            color: #fff;
        }
        .chart {
            width: 50%;
            margin: 20px auto;
        }
    </style>
</head>
<body>
    <h1>Indian Stocks</h1>
    <div class="chart">
        <img src="{{ chart_url }}" alt="Stock Chart">
    </div>
    <table>
        <tr>
            <th>Stock</th>
            <th>Price</th>
            <th>Change</th>
        </tr>
        {% for stock in stocks %}
        <tr>
            <td>{{ stock['symbol'] }}</td>
            <td>{{ stock['price'] }}</td>
            <td style="color: {% if stock['change'] > 0 %}blue{% else %}yellow{% endif %};">{{ stock['change'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def index():
    try:
        # Fetch stock data
        stocks = []
        for stock in indian_stocks:
            try:
                ticker = yf.Ticker(stock)
                data = ticker.history(period='1d')
                if not data.empty:
                    if isinstance(data.columns, pd.MultiIndex):
                        data.columns = data.columns.get_level_values(0)
                    price = data['Close'].iloc[-1]
                    change = data['Close'].iloc[-1] - data['Open'].iloc[-1]
                    stocks.append({'symbol': stock, 'price': price, 'change': change})
            except Exception as e:
                print(f'Error fetching {stock}: {e}')
        
        # Generate chart
        if stocks:
            fig, ax = plt.subplots()
            changes = [stock['change'] for stock in stocks]
            ax.bar([stock['symbol'] for stock in stocks], changes, color=['blue' if change > 0 else 'yellow' for change in changes])
            ax.set_title('Indian Stocks')
            ax.set_xlabel('Stock')
            ax.set_ylabel('Change')
            ax.tick_params(axis='x', rotation=90)
            
            # Save chart to bytes
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            chart_url = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close(fig)
        else:
            chart_url = ''
        
        # Render template
        return render_template_string(html_template, chart_url=f'data:image/png;base64,{chart_url}', stocks=stocks)
    
    except Exception as e:
        return 'Error: {}'.format(e)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)