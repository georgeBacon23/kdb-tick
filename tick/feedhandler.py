import json
import logging
import numpy as np

from alpaca.data.live import CryptoDataStream
from qpython import qconnection
from qpython.qcollection import qlist 
from qpython.qtype import QDOUBLE_LIST, QSYMBOL_LIST, QTIMESPAN_LIST

logger = logging.getLogger(__name__)

def get_creds():
    creds_file = 'tick/creds.json'
    with open(creds_file) as f:
        return json.load(f)

def get_timedelta(datetime):
    return np.datetime64(datetime.replace(tzinfo=None), 'ns') - np.datetime64('today')

def crypto_quote(quote):
    logger.info('raw crypto quote: %s', quote)
    times = qlist([get_timedelta(quote.timestamp)], qtype=QTIMESPAN_LIST)
    symbols = qlist([quote.symbol], qtype=QSYMBOL_LIST)
    bids = qlist([quote.bid_price], qtype=QDOUBLE_LIST)
    asks = qlist([quote.ask_price], qtype=QDOUBLE_LIST)
    bid_sizes = qlist([quote.bid_size], qtype=QDOUBLE_LIST)
    ask_sizes = qlist([quote.ask_size], qtype=QDOUBLE_LIST)
    return [times, symbols, bids, asks, bid_sizes, ask_sizes]

def crypto_trade(trade):
    logger.info('raw crypto trade: %s', trade)
    times = qlist([get_timedelta(trade.timestamp)], qtype=QTIMESPAN_LIST)
    symbols = qlist([trade.symbol], qtype=QSYMBOL_LIST)
    prices = qlist([trade.price], qtype=QDOUBLE_LIST)
    sizes = qlist([trade.size], qtype=QDOUBLE_LIST)
    return [times, symbols, prices, sizes]

def main():
    logging.basicConfig(level=logging.INFO)
    creds = get_creds()
    wss_client = CryptoDataStream(creds['APCA_API_KEY_ID'], 
                                  creds['APCA_API_SECRET_KEY'])  
    
    symbols = ['AAVE', 'ALGO', 'BAT', 'BCH', 'BTC', 'DAI', 'ETH', 'GRT', 'LINK', 'LTC']

    with qconnection.QConnection(host='localhost', port=5010) as qcon:
        async def process_crypto_trade(trade):
            qcon.sendSync('.u.upd', np.string_('cryptotrades'), crypto_trade(trade))

        async def process_crypto_quote(quote):
            qcon.sendSync('.u.upd', np.string_('cryptoquotes'), crypto_quote(quote))
        
        for symbol in symbols:
            wss_client.subscribe_trades(process_crypto_trade, f'{symbol}/USD')
            wss_client.subscribe_quotes(process_crypto_quote, f'{symbol}/USD')

        wss_client.run()

if __name__ == "__main__":
    main()



