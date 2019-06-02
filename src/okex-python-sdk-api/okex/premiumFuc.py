#coding=utf-8
import account_api as account
import ett_api as ett
import futures_api as future
import lever_api as lever
import spot_api as spot
import swap_api as swap
import json
import pymysql.cursors
from consts import *
from datetime import datetime,timedelta
from database import *

def futrueCoinList (accounts):
    jsonFutureAccount = json.dumps(accounts)
    dictFutureAccount = json.loads(jsonFutureAccount)

    coinList = futureAccountCoinList(dictFutureAccount)  # 期货合约币种列表
    return coinList

def maxDateFuture(futureResultTicker):
    jsonFutureTicker = json.dumps(futureResultTicker)
    dictFutureTicker = json.loads(jsonFutureTicker)
    maxDate = 0
    for futureTicker in dictFutureTicker:
        if (maxDate < futureTicker['instrument_id'].split('-', 3)[2]):
            maxDate = futureTicker['instrument_id'].split('-', 3)[2]

    return maxDate

def premiumInformation(timestamp,futureResultTicker,swapResultTicker,maxDate):

    jsonFutureTicker = json.dumps(futureResultTicker)
    dictFutureTicker = json.loads(jsonFutureTicker)
    ft = {}

    for futureTicker in dictFutureTicker:
        instrument = futureTicker['instrument_id']
        timestamp['timestamp'] = futureTicker['timestamp']
        futureKey = instrument.split('-', 3)[0] + "-USD" + "-" + maxDate
        if futureKey == instrument:
            ft[futureTicker['instrument_id'].split('-', 3)[0] + "-USD"] = float(futureTicker['last'])

    jsonSwapTicker = json.dumps(swapResultTicker)
    dictSwapTicker = json.loads(jsonSwapTicker)

    st = {}
    for swapTicker in dictSwapTicker:
        instrument = swapTicker['instrument_id'];
        swapKey = instrument.split('-', 3)[0] + "-USD"
        st[swapKey] = float(swapTicker['last'])

    premiumDict = {}
    for coin in COIN_LIST:
        # print coin
        premiumDict[coin] = (ft[coin] - st[coin]) / st[coin]

    try:
        date_ = datetime.strptime(timestamp['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
        local_time = date_ + timedelta(hours=8)

        local_time.strftime("%Y-%m-%d %H:%M:%S")
        timestamp['timestamp'] = local_time

    except:
        print "date_ failed"

    # local_time = 2018-08-06 18:00:00

    return premiumDict

def futureAccountCoinList(dictFutureAccount):

    coinList = []

    for coin in dictFutureAccount['info']:
        coinList.append(coin)

    return coinList

# 合约信息的收益权益
def futureRealizedAccountCoinInfor(dictRealizedFutureCoin,coinList,dictFutureAccount):

    for coin in coinList:
        # print dictFutureAccount['info'][coin]['equity']
        dictRealizedFutureCoin[coin] = float(dictFutureAccount['info'][coin]['equity']  )

#目前持仓的币数
def futureAvailableAccountCoinInfor(dictAvailableFutureCoin,coinList,futureAPI,futureMaxDate):
    dictCoinInformation = {}
    coinPrice = {}

    for coin in coinList:
        coinKey = coin + "-USD" + "-" + str(futureMaxDate)
        indexPrice = futureAPI.get_index(coinKey)
        print "indexPrice:"+str(indexPrice)
        coinPrice[coin] = float(indexPrice['index'])
        infor = futureAPI.get_specific_position(coinKey)
        dictCoinInformation[coin] = infor
        if infor['holding'][0]['short_qty'] == 0:
            if coin == 'BTC':
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['long_qty']) * 100
            else:
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['long_qty']) * 10
        else:
            if coin == 'BTC':
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['short_qty']) * 100
            else:
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['short_qty']) * 10
    return coinPrice

def futureCoinInformation(futureAPI,accounts,dictRealizedFutureCoin,dictAvailableFutureCoin,dictPriceDifference,futureMaxDate):

    jsonFutureAccount = json.dumps(accounts)
    dictFutureAccount = json.loads(jsonFutureAccount)

    coinList = futureAccountCoinList(dictFutureAccount) #期货合约币种列表

    print dictFutureAccount
    futureRealizedAccountCoinInfor(dictRealizedFutureCoin, coinList, dictFutureAccount)
    coinPrice = futureAvailableAccountCoinInfor(dictAvailableFutureCoin, coinList,futureAPI,futureMaxDate)

    for coin in coinList:
        print str(dictRealizedFutureCoin[coin]) + "--" + str(dictAvailableFutureCoin[coin])
        dictPriceDifference[coin] = float(abs(dictRealizedFutureCoin[coin] - dictAvailableFutureCoin[coin]))

    return dictPriceDifference

def futurePosition(futureAPI,accounts,dictAvailableFutureCoin,futureMaxDate):
    dictPricePosition = {}
    jsonFutureAccount = json.dumps(accounts)
    dictFutureAccount = json.loads(jsonFutureAccount)

    coinList = futureAccountCoinList(dictFutureAccount) #期货合约币种列表

    coinPrice = futureAvailableAccountCoinInfor(dictAvailableFutureCoin, coinList,futureAPI,futureMaxDate)

    for coin in coinList:
        print
        dictPricePosition[coin] = float(abs(dictAvailableFutureCoin[coin]))

    # print dictPricePosition
    return dictPricePosition


def discoverPremiumOpportunities(priceList,db,timestamp,futureResultTicker,swapResultTicker,futureMaxDate):

    endLowPriceList = {}
    endMidPriceList = {}
    endGoodPriceList = {}
    endWonderPriceList = {}

    for price in priceList:
        if abs(price[1]) >= 0.018:
            endLowPriceList[price[0]] = price[1]
        if abs(price[1]) >= 0.023:
            endMidPriceList[price[0]] = price[1]
        if abs(price[1]) >= 0.03:
            endGoodPriceList[price[0]] = price[1]
        if abs(price[1]) >= 0.05:
            endWonderPriceList[price[0]] = price[1]

    endLowPriceList = sorted(endLowPriceList.items(), key=lambda d: d[1], reverse=True)
    endMidPriceList = sorted(endMidPriceList.items(), key=lambda d: d[1], reverse=True)
    endGoodPriceList = sorted(endGoodPriceList.items(), key=lambda d: d[1], reverse=True)
    endWonderPriceList = sorted(endWonderPriceList.items(), key=lambda d: d[1], reverse=True)

    return 1

def judgingTrade(coinBigPriceList,coinAVGList):
    for coin in coinBigPriceList:
        if (abs(coinBigPriceList[coin]) > 0.015):
            if coinBigPriceList[coin] >= coinAVGList[coin]:
                return 1
            elif coinBigPriceList[coin] < coinAVGList[coin]:
                return 0


