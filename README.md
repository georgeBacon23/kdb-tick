## Purpose

This repo provides an easy way to experiment and learn kdb+tick using real market data. It is not meant to be production code, just a basic setup for those that want to practice qsql against real data.

## Contents

Vanilla kdb+tick setup (i.e. tickerplant and RDB) with a Python based 'feedhandler'. The feedhandler gets crypto data from Alpaca via websocket and uses qpython to write it to the tickerplant. Crypto was chosen as it's traded 24/7, so experimentation isn't limited to market opening hours.

See https://alpaca.markets/docs/api-references/market-data-api/ for more information regarding Alpaca market data APIs.

See https://code.kx.com/q/wp/rt-tick/ for more information regarding kdb+tick.

## API Requirements

An Alpaca API key is required to run the feedhandler. At the time of writing, this can be obtained for free to allow access to enough data for testing purposes, see https://alpaca.markets/data.

## Setup Python environment

Create a virtual environment with the relevant packages:

```sh
python3.9 -m venv kdbtick
source kdbtick/bin/activate
pip install -r requirements.txt
```

Note, tested with Python 3.9. 

## Run ticker plant and RDB

Start the ticker plant process: 

```sh 
~/q64/l64/q tick.q sym db -p 5010
```

adjusting q path accordingly.

From another terminal, start the RDB:

```sh
rlwrap ~/q64/l64/q tick/r.q -p 5011
```

We use `rlwrap` in the latter for easy line editing/history etc, as we will directly run queries in the resulting q session. 

## Run feed handler

Set `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` in `creds.json` (Alpaca API creds), then in another terminal:

```sh
python tick/feedhandler.py
```

Typical output:

```
INFO:alpaca.common.websocket:started data stream
INFO:alpaca.common.websocket:starting data websocket connection
INFO:alpaca.common.websocket:connected to: wss://stream.data.alpaca.markets/v1beta2/crypto
INFO:alpaca.common.websocket:subscribed to trades: ['LINK/USD', 'DAI/USD', 'BTC/USD', 'BAT/USD', 'BCH/USD', 'ETH/USD', 'GRT/USD', 'LTC/USD', 'AAVE/USD', 'ALGO/USD'], quotes: ['BAT/USD', 'DAI/USD', 'AAVE/USD', 'BTC/USD', 'ALGO/USD', 'LINK/USD', 'LTC/USD', 'BCH/USD', 'ETH/USD', 'GRT/USD'], bars: [], updatedBars: [], dailyBars: []
INFO:__main__:raw crypto quote: symbol='BTC/USD' timestamp=datetime.datetime(2023, 2, 5, 20, 44, 33, 534890, tzinfo=datetime.timezone.utc) ask_exchange=None ask_price=22878.36 ask_size=0.04 bid_exchange=None bid_price=22873.26 bid_size=0.152562 conditions=None tape=None
INFO:__main__:raw crypto quote: symbol='LTC/USD' timestamp=datetime.datetime(2023, 2, 5, 20, 44, 33, 563058, tzinfo=datetime.timezone.utc) ask_exchange=None ask_price=95.29 ask_size=2.4 bid_exchange=None bid_price=95.28 bid_size=2.0 conditions=None tape=None
...
```

Note, we assume the kdbtick virtual environment has been activated.

## View data in RDB

From RDB terminal,

Quotes:

```q
q)last select from cryptoquotes
time | 0D20:44:33.695745000
sym  | `BTC/USD
bid  | 22873.27
ask  | 22878.36
bsize| 0.072814
asize| 0.052565
```

Trades:

```q
q)last select from cryptotrades
time | 0D20:44:27.549000000
sym  | `BTC/USD
price| 22878.56
size | 0.003525
```

## Notes

Again, this is purely for learning purposes. In general one might wish to run the processes in the background and use `nohup` to avoid termination on shell exits. In that case we could connect to the RDB using IPC.  