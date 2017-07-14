#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017  Bernhard Hörl www.bernhardhoerl.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import gdax
import sys
import argparse


def coinprice (currency_pair, warning, critical, moon, perfdata):

    if currency_pair == "eth_eur":
        productid = "ETH-EUR"
        coin = "ETH"
        fiat = "EUR"
    elif currency_pair == "eth_usd":
        productid = "ETH-USD"
        coin = "ETH"
        fiat = "USD"
    elif currency_pair == "btc_eur":
        productid = "BTC-EUR"
        coin = "BTC"
        fiat = "EUR"
    elif currency_pair == "btc_usd":
        productid = "BTC-USD"
        coin = "BTC"
        fiat = "USD"
    elif currency_pair == "ltc_eur":
        productid = "LTC-EUR"
        coin = "LTC"
        fiat = "EUR"
    elif currency_pair == "ltc_usd":
        productid = "LTC-USD"
        coin = "LTC"
        fiat = "USD"

    public_client = gdax.PublicClient()
    price = float(public_client.get_product_ticker(product_id=productid)["price"])
    price_msg = str(price) + " " + fiat
    price_msg_perfdata = str(price) + " " + fiat + " | " + coin + "/" + fiat + "=" + str(price)

    if price < critical:
        if perfdata:
            print "CRITICAL! " + price_msg_perfdata
            sys.exit(2)
        print "CRITICAL! " + price_msg
        sys.exit(2)
    elif price < warning:
        if perfdata:
            print "WARNING! " + price_msg_perfdata
            sys.exit(1)
        print "WARNING! " + price_msg
        sys.exit(1)
    elif moon:
        if price > moon:
            if perfdata:
                print "MOON! " + price_msg_perfdata
                sys.exit(2)
            print "MOON! " + price_msg
            sys.exit(2)
    
    if perfdata:
        print "OK " + price_msg_perfdata
        sys.exit(0)
    else:
        print "OK " + price_msg
        sys.exit(0)


def main ():

    parser = argparse.ArgumentParser(
        description="Check the price of various cryptocurrencies.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=('''Examples:
  check_coin_price.py -p eth_eur -w 100 -c 50
  check_coin_price.py -p btc_usd -w 1500 -c 1000 -f
  check_coin_price.py -p btc_usd -w 1500 -c 1000 -f -m 5000
        '''))

    parser._optionals.title = "Arguments"

    parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    parser.add_argument("-p", dest="currency_pair", required=True,
                  choices=["eth_eur", "eth_usd", "btc_eur", "btc_usd", "ltc_eur", "ltc_usd"],
                  help="scpecify currency pair")
    parser.add_argument("-w",
                  dest="warning", type=float, required=True,
                  help="warning if price drops below this value")
    parser.add_argument("-c",
                  dest="critical", type=float, required=True,
                  help="critical if price drops below this value")
    parser.add_argument("-m",
                  dest="moon", type=float,
                  help="critical if price rise above this value")
    parser.add_argument("-f",
                  action="store_true", dest="perfdata",
                  help="enable nagios performance data output")

    args = parser.parse_args()

    if args.critical > args.warning:
        parser.print_usage()
        print __file__ + ": error: value of cirtical must be lower than warning"
        sys.exit(3)

    coinprice(args.currency_pair, args.warning, args.critical, args.moon, args.perfdata)

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print str(error)
        sys.exit(3)