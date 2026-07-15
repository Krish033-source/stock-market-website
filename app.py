from flask import Flask
import yfinance as yf
import matplotlib
import numpy as np
import pandas as pd
import random
import io
import base64
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'change_this_to_a_random_secret_key'  # CHANGE THIS TO A RANDOM SECRET KEY

def get_random_stocks(n):
    stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB', 'TSLA', 'BABA', 'JPM', 'V', 'MA']
    return random.sample(stocks, n)

def get_stock_data(stock):
    data = yf.download(stock, period='1d', interval='1m')
    return data

def plot_stock_data(data, stock):
    img = io.BytesIO()
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'])
    plt.title(stock)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid(True)
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()

def get_stock_profit_loss(data):
    if data['Close'].iloc[-1] > data['Open'].iloc[0]:
        return 'profit', 'yellow'
    else:
        return 'loss', 'blue'

def generate_chart(data, stock):
    plot = plot_stock_data(data, stock)
    profit_loss, color = get_stock_profit_loss(data)
    return plot, profit_loss, color

def generate_charts(n):
    stocks = get_random_stocks(n)
    charts = []
    for stock in stocks:
        data = get_stock_data(stock)
        plot, profit_loss, color = generate_chart(data, stock)
        charts.append((stock, plot, profit_loss, color))
    return charts

@app.route('/')
def index():
    charts = generate_charts(10)
    html = '''
    <html>
    <head>
        <title>Stock Charts</title>
        <style>
            body {
                background-color: #333;
                color: #fff;
            }
            .chart {
                margin: 20px;
            }
        </style>
    </head>
    <body>
    '''
    for stock, plot, profit_loss, color in charts:
        html += '''
        <div class="chart">
            <h2>{}</h2>
            <img src="data:image/png;base64,{}">
            <p>{}: <span style="color:{}">{}</span></p>
        </div>
        '''.format(stock, plot, 'Profit' if profit_loss == 'profit' else 'Loss', color, profit_loss)
    html += '''
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    app.run(debug=True)