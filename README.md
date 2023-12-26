# Stock Return Comparison Tool
Overview
This Streamlit-based web application allows users to compare the performance of any stock against major indices like SPY (S&P 500) and QQQ (NASDAQ-100). The application fetches real-time data using yfinance and visualizes the stock's return since a user-defined date, normalized against these indices.

# Features
User Input for Stock Ticker and Start Date: Allows users to input any stock ticker and select a start date for comparison.
Real-time Data Fetching: Leverages yfinance to fetch real-time stock data.
Interactive Visualization: Uses altair for generating an interactive line chart that compares the normalized stock price performance of the selected stock with SPY and QQQ.

# Installation
To run this application locally, you need to have Python installed along with the following packages:
* streamlit
* yfinance
* pandas
* altair
You can install these packages using pip:

# How to Run
After installing the required packages, you can run the application using Streamlit.
