#coding=utf-8
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import okex.account_api as account
import okex.ett_api as ett
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import json
from datetime import datetime,timedelta
from okex.consts import *
from okex.premiumFuc import *
from okex.database import *
if __name__ == '__main__':


    dictRealizedFutureCoin = {}
    dictAvailableFutureCoin = {}
    dictPriceDifference = {}
    coinSTDList = {}
    coinAVGList = {}
    coinBigPriceList = {}
    priceList = {}

    api_key = API_KEY
    seceret_key = SECERET_KEY
    passphrase = PASSPARASE

    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)  #登陆期货合约
    swapAPI = swap.SwapAPI(api_key, seceret_key, passphrase, True) #登陆永续期货合约
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DBNAME) #连接数据库

    count = 0
    type = 0  #0未开单，1已开单

    while True:
        try:
            # 定义
            dictRealizedFutureCoin = {}
            dictAvailableFutureCoin = {}
            dictPriceDifference = {}
            message = ""
            timestamp = {}
            coinAVGList = {}
            coinBigPriceList = {}
            priceList = {}

            accounts = futureAPI.get_accounts()
            futureResultTicker = futureAPI.get_ticker()
            swapResultTicker = swapAPI.get_ticker()
            futureMaxDate = maxDateFuture(futureResultTicker)

            # 每日刷新一次，获取波动的标准差
            if count % 2880 == 0:
                print "更新标准差列表"
                coinSTDList = {}
                resultSDT = gettingPremiumSTD(db)
                for r in resultSDT:
                    coinSTDList[r[0]] = r[1]

            # 获取溢价列表
            priceList = premiumInformation(timestamp, futureResultTicker, swapResultTicker, futureMaxDate)
            # 插入数据库
            premiumInsert(db, priceList, timestamp)

            # 获取波动较大的3个溢价列表 !!!!
            for coin in coinSTDList:
                coinBigPriceList[coin] = priceList[coin]

            # 每30s刷新一次，获取溢价平均值 !!!!
            resultAVG = gettingPremiumAVGPositive(db)
            for a in resultAVG:
                coinAVGList[a[0]] = a[1]

            print coinBigPriceList
            print coinAVGList

            #判断是否进行交易
            if type ==0 :
                whetherTrade = judgingTrade(coinBigPriceList,coinAVGList)
                print whetherTrade

                #用户买入现货操作（mort）
                #做空做多期货和永续（yan）

                type =1

            elif type ==1:




        except:
            print "error failed"


        time.sleep(30)  # 30s一次

