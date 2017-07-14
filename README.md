# check_coin_price
Nagios plugin to check the price of various cryptocurrencies (can also be used stand-alone from cli).<br>
(Python Version 2.7)

## Install required python packages
`pip install gdax`

## Usage
`python check_coin_price.py --help`
```
usage: check_coin_price.py [-h] [--version] -p
                           {eth_eur,eth_usd,btc_eur,btc_usd,ltc_eur,ltc_usd}
                           -w WARNING -c CRITICAL [-m MOON] [-f]

Check the price of various cryptocurrencies.

Arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -p {eth_eur,eth_usd,btc_eur,btc_usd,ltc_eur,ltc_usd}
                        scpecify currency pair
  -w WARNING            warning if price drops below this value
  -c CRITICAL           critical if price drops below this value
  -m MOON               critical if price rise above this value
  -f                    enable nagios performance data output

Examples:
  check_coin_price.py -p eth_eur -w 100 -c 50
  check_coin_price.py -p btc_usd -w 1500 -c 1000 -f
  check_coin_price.py -p btc_usd -w 1500 -c 1000 -f -m 5000
```
