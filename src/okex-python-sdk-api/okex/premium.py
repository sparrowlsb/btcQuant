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

    premiumDict = sorted(premiumDict.items(), key=lambda d: d[1], reverse=True)

    date_ = datetime.strptime(timestamp['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # local_time = 2018-08-06 18:00:00

    local_time = date_ + timedelta(hours=8)

    local_time.strftime("%Y-%m-%d %H:%M:%S")
    timestamp['timestamp'] = local_time

    return premiumDict

def futureAccountCoinList(dictFutureAccount):

    coinList = []

    for coin in dictFutureAccount['info']:
        coinList.append(coin)

    return coinList

def futureAccountCoinInfor(dictRealizedFutureCoin,coinList,dictFutureAccount):

    for coin in coinList:
        # print dictFutureAccount['info'][coin]['equity']
        dictRealizedFutureCoin[coin] = float(dictFutureAccount['info'][coin]['equity']  )

def futureCoinInformation(futureAPI,accountsAPI,dictRealizedFutureCoin,dictAvailableFutureCoin,dictPriceDifference,futureMaxDate):
    jsonFutureAccount = json.dumps(accountsAPI)
    dictFutureAccount = json.loads(jsonFutureAccount)
    coinList = futureAccountCoinList(dictFutureAccount)
    dictCoinInformation = {}
    # print dictFutureAccount
    futureAccountCoinInfor(dictRealizedFutureCoin, coinList, dictFutureAccount)

    for coin in coinList:
        coinKey = coin + "-USD" + "-" + str(futureMaxDate)
        indexPrice = futureAPI.get_index(coinKey)
        # print indexPrice
        coinPrice = float(indexPrice['index'])
        infor = futureAPI.get_specific_position(coinKey)
        dictCoinInformation[coin] = infor
        if  infor['holding'][0]['short_qty']==0:
            if coin=='BTC':
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['long_qty'])*100/coinPrice
            else:
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['long_qty']) * 10/coinPrice
        else:
            if coin=='BTC':
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['short_qty'])*100/coinPrice
            else:
                dictAvailableFutureCoin[coin] = float(infor['holding'][0]['short_qty']) * 10/coinPrice
    # print 1111
    # print dictAvailableFutureCoin
    #
    # print dictRealizedFutureCoin
    # print dictAvailableFutureCoin

    # print coinList
    for coin in coinList:
        # print str(dictRealizedFutureCoin[coin]) + "--" + str(dictAvailableFutureCoin[coin])
        dictPriceDifference[coin] = float(abs(dictRealizedFutureCoin[coin] - dictAvailableFutureCoin[coin])*coinPrice)

    return dictPriceDifference

def premiumInsert(db,priceList,timestamp):
    cursor = db.cursor()

    for price in priceList:
        # SQL 插入语句
        sql = 'insert into premium_information(coin_name,premium_price,premium_data) values(\'%s\',\'%s\' ,\'%s\')' % (price[0], price[1],timestamp['timestamp'])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
        except:
            # Rollback in case there is any error
            print 'premiumInsert error'
            db.rollback()

def premiumAnalysis(db):
    cursor = db.cursor()


    # SQL 插入语句
    sql = 'select * from premium_information order by id  '

    # premiumCoinList['']
    try:
        # 执行sql语句
        cursor.execute(sql)


        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        # Rollback in case there is any error
        print 'premiumInsert error'
        db.rollback()

def distinctTime(db):
    cursor = db.cursor()

    # SQL 插入语句
    sql = 'select distinct(premium_data ) from premium_information order by id  '

    # premiumCoinList['']
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        # Rollback in case there is any error
        print 'premiumInsert error'
        db.rollback()
