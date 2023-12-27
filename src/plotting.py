import plotly.graph_objs as go


def plot_candles(df):
    figure = go.Figure(go.Candlestick(x=df["time"], open=df["open"], high=df["high"], low=df["low"], close=df["close"]))
    figure.update_layout(title="Candlestick Chart")
    return figure

def calculate_stochastic(df, period_k=14, period_d=3):
    low_rolling_min = df['low'].rolling(window=period_k).min()
    high_rolling_max = df['high'].rolling(window=period_k).max()

    df['%K'] = ((df['close'] - low_rolling_min) / (high_rolling_max - low_rolling_min)) * 100
    df['%D'] = df['%K'].rolling(window=period_d).mean()

    return df

def plot_stochastic(df):
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=df["time"], y=df["%K"], mode="lines", name="%K"))
    figure.add_trace(go.Scatter(x=df["time"], y=df["%D"], mode="lines", name="%D", line=dict(color='red')))
    figure.update_layout(title="Stochastic Oscillator Chart and its Moving Average")
    return figure

def plot_combination(df):
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=df["time"], y=df["%K"], mode="lines", name="%K", yaxis="y1"))
    figure.add_trace(go.Scatter(x=df["time"], y=df["%D"], mode="lines", name="%D", line=dict(color='red'), yaxis="y1"))
    figure.add_trace(go.Scatter(x=df["time"], y=df["close"], mode="lines", name="Price", line=dict(color='green'), yaxis="y2"))
    figure.update_layout(
        yaxis=dict(title="%K and %D", side="left", showgrid=False, zeroline=False),
        yaxis2=dict(title="Price", overlaying='y', side='right', showgrid=False, zeroline=False),
        xaxis=dict(title="Date"),
        legend=dict(x=1.1, y=1),
        title="Price and Stochastic Oscillator Chart"
    )
    return figure
