# Import libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# Set up the streamlit interface
st.title("Stock return against indices") 

# Get the ticker and the start date
ticker = st.text_input("Enter a stock ticker", value="RELY")  # Default set to Apple
start_date = st.date_input("Select a start date", value=pd.to_datetime("2023-01-01"))  # Default set to Jan 1, 2023

# Define colors and line thickness
colors = {
    ticker: 'orange',
    'SPY': 'grey',
    'QQQ': 'lightblue'
}
line_thickness = {
    ticker: 3,
    'SPY': 1.5,
    'QQQ': 1.5
}

# Fetch the stock data
if st.button('Fetch Data'):
    def fetch_and_normalize_data(ticker, start_date):
        data = yf.download(ticker, start=start_date)
        data.reset_index(inplace=True)  # Reset the index to turn 'Date' into a column
        data['Normalized Close'] = (data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0]
        return data

    tickers = [ticker, "SPY", "QQQ"]
    source = pd.DataFrame()
    for entry in tickers:
        data = fetch_and_normalize_data(entry, start_date)
        data['Ticker'] = entry
        source = pd.concat([source, data])

    # Ensure Date is a datetime type for Altair
    source['Date'] = pd.to_datetime(source['Date'])

    # Altair Chart
    chart = alt.Chart(source).mark_line().encode(
        x='Date:T',
        y='Normalized Close:Q',
        color=alt.Color('Ticker:N', scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values()))),
        strokeWidth=alt.StrokeWidth('Ticker:N', scale=alt.Scale(domain=list(line_thickness.keys()), range=list(line_thickness.values())))
    ).properties(
        title='Stock Price Performance Comparison',
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)
