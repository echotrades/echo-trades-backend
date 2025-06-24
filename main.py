from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import yfinance as yf
import random
from datetime import date, timedelta

app = FastAPI()

class TradePick(BaseModel):
    ticker: str
    type: str
    strike: float
    expiry: str
    entry: float
    exit: float
    confidence: int
    analysis: str

def generate_analysis(ticker, history):
    last_close = history['Close'].iloc[-1]
    avg_volume = history['Volume'].mean()
    recent_volume = history['Volume'].iloc[-1]
    price_trend = "uptrend" if history['Close'].iloc[-1] > history['Close'].mean() else "downtrend"

    return f"{ticker} is in a {price_trend} with closing price ${last_close:.2f}. " +            f"Recent volume {recent_volume:,} vs avg {int(avg_volume):,}. Potential volatility."

@app.get("/generate-picks", response_model=List[TradePick])
def generate_picks():
    tickers = ["AAPL", "NVDA", "TSLA", "MSFT"]
    picks = []
    expiry_date = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="10d")

        if hist.empty:
            continue

        last_price = hist['Close'].iloc[-1]
        strike = round(last_price * (1.05 if random.random() > 0.5 else 0.95), 2)
        option_type = "Call" if strike > last_price else "Put"
        entry = round(random.uniform(0.9, 1.8), 2)
        exit_target = round(entry * random.uniform(1.3, 2.0), 2)

        picks.append(TradePick(
            ticker=ticker,
            type=option_type,
            strike=strike,
            expiry=expiry_date,
            entry=entry,
            exit=exit_target,
            confidence=random.randint(7, 10),
            analysis=generate_analysis(ticker, hist)
        ))

    return picks