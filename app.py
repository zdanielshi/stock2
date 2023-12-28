# Import libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

# Define the function to load "About" content
def load_about():
    with open('about.txt', 'r') as file:
        about_text = file.read()
    return about_text

# Define function to get ticker data
def fetch_and_normalize_data(ticker, start_date):
    data = yf.download(ticker, start=start_date)
    data.reset_index(inplace = True)
    data['Normalized Close'] = (data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0]
    return data

# Function to get colors for user tickers
def get_colors(n):
    color_map = plt.cm.get_cmap('tab20', n)
    return [color_map(i/n) for i in range(n)]  # Generate a list of colors

# Set up the Streamlit interface
st.title("Stock returns comparison")

about_section = load_about()
st.sidebar.markdown(about_section, unsafe_allow_html = True)

# Get ticker and start date from user
ticker_input = st.text_input("Enter stock ticker(s). Up to 10, separated by commas", 
                            value = "RELY",
                            help = "You can enter more than 10, but the app will only evaluate the first 10.")
start_date = st.date_input("Select a start date",
                            value = pd.to_datetime("2023-01-01"))

# Process the ticker input from the user, and chop it off at 10
user_tickers = [ticker.strip().upper() for ticker in ticker_input.split(',')][:10] # Takes only the first 10 tickers

# Always include SPY and QQQ
tickers = ['SPY', 'QQQ']
tickers.extend(user_tickers)

# Generate a list of colors for the user-entered tickers
color_list = get_colors(len(user_tickers))

# Create a dictionary to map each ticker to its color
colors_hex = {ticker: mcolors.to_hex(color_list[i]) for i, ticker in enumerate(user_tickers)}

# Assign specific colors for SPY and QQQ
colors_hex['SPY'] = 'black'
colors_hex['QQQ'] = '#8B0000'  # Dark red

# Seat the Seaborn style
sns.set(style = "whitegrid")

# Button to fetch data
if st.button('Fetch Data'):
    source = pd.DataFrame()
    
    # Fetch the data for each ticker
    for ticker in tickers:
        data = fetch_and_normalize_data(ticker, start_date)
        if data is not None:
            data['Ticker'] = ticker
            source = pd.concat([source, data])
    
    source['Date'] = pd.to_datetime(source['Date'])

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot data for each user-entered ticker using Seaborn's color palette
    palette = sns.color_palette("tab10", n_colors=len(user_tickers))
    for i, ticker in enumerate(user_tickers):
        ticker_data = source[source['Ticker'] == ticker]
        ax.plot(ticker_data['Date'], ticker_data['Normalized Close'], label=ticker, color=palette[i])

    # Plot data for SPY and QQQ with specific styles
    for ticker in ['SPY', 'QQQ']:
        ticker_data = source[source['Ticker'] == ticker]
        color = 'black' if ticker == 'SPY' else '#8B0000'  # Black for SPY, Dark Red for QQQ
        ax.plot(ticker_data['Date'], ticker_data['Normalized Close'], label=ticker, color=color, linewidth=4)

    # Customize the chart
    ax.set_title('Stock Price Performance Comparison')
    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Close')
    ax.legend()

    # Display the chart in Streamlit
    st.pyplot(fig)