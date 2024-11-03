from backend.download_data import fill_funding, fill_open_interest, fill_interest
from backend.models.models_orm import Coin, Symbol


if __name__ == "__main__":
    for symbol in Symbol:
        
        fill_funding(symbol)
        fill_open_interest(symbol)

    for coin in Coin:

        fill_interest(coin)