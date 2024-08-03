import yfinance as yf

def get_currency_value_att(currency):
    try:
        ticker_symbol = f"{currency}=X"
        ticker = yf.Ticker(ticker_symbol)
        hist = ticker.history(period="1d")

        if hist.empty:
            raise ValueError(f"No data for currency {currency}")

        current_value = hist['Close'][0]

        return current_value
    except Exception as ex:
        raise ValueError(f"Error on currency {currency}: {str(ex)}")
