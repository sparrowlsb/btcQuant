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
from okex.premium import *
if __name__ == '__main__':

    api_key = API_KEY
    seceret_key = SECERET_KEY
    passphrase = PASSPARASE

    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
    swapAPI = swap.SwapAPI(api_key, seceret_key, passphrase, True)

    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DBNAME)

    count = 0
    while True:

        # future api test
        dictRealizedFutureCoin = {}
        dictAvailableFutureCoin = {}
        dictPriceDifference = {}
        message = ""
        timestamp = {}

        # print message


        accountsAPI = futureAPI.get_accounts()

        futureResultTicker = futureAPI.get_ticker()
        swapResultTicker = swapAPI.get_ticker()
        # 合约季度时间
        futureMaxDate = maxDateFuture(futureResultTicker)
        # 溢价排序
        priceList = {}
        priceList = premiumInformation(timestamp,futureResultTicker,swapResultTicker,futureMaxDate)

        premiumInsert(db,priceList,timestamp)
        print priceList

        endLowPriceList = {}
        endMidPriceList = {}
        endGoodPriceList = {}
        endWonderPriceList = {}

        for price in  priceList:
            if price[1]>=0.018 :
                endLowPriceList[price[0]]=price[1]
            if price[1] >= 0.023:
                endMidPriceList[price[0]] = price[1]
            if price[1] >= 0.03:
                endGoodPriceList[price[0]] = price[1]
            if price[1] >= 0.05:
                endWonderPriceList[price[0]] = price[1]

        endLowPriceList = sorted(endLowPriceList.items(), key=lambda d: d[1], reverse=True)
        endMidPriceList = sorted(endMidPriceList.items(), key=lambda d: d[1], reverse=True)
        endGoodPriceList = sorted(endGoodPriceList.items(), key=lambda d: d[1], reverse=True)
        endWonderPriceList = sorted(endWonderPriceList.items(), key=lambda d: d[1], reverse=True)

        # print endLowPriceList

        if endWonderPriceList :
            s = ""
            for price in endWonderPriceList:
                s = s +"币种："+str(price[0])+ " 溢价率："+str(price[1])+"\n"
            print s
            message = MIMEText((s), "plain", "utf-8")

            message["Subject"] = "quant 溢价超过5个点 千载难逢交易机会"
            message["To"] = EMAIL_FROM
            message["From"] = EMAIL_FROM

        elif endGoodPriceList and count % 10 == 0:
            s = ""
            for price in endGoodPriceList:
                s = s + "币种：" + str(price[0]) + " 溢价率：" + str(price[1]) + "\n"
            print s
            message = MIMEText((s), "plain", "utf-8")

            message["Subject"] = "quant 溢价超过3个点 很好的交易机会"
            message["To"] = EMAIL_FROM
            message["From"] = EMAIL_FROM

        elif endMidPriceList and count % 60 == 0:
            s = ""
            for price in endMidPriceList:
                s = s + "币种：" + str(price[0]) + " 溢价率：" + str(price[1]) + "\n"
            print s
            message = MIMEText((s), "plain", "utf-8")

            message["Subject"] = "quant 溢价超过2.3个点 一般交易机会"
            message["To"] = EMAIL_FROM
            message["From"] = EMAIL_FROM

        elif endLowPriceList and count % 120 == 0:
            s = ""
            for price in endLowPriceList:
                s = s + "币种：" + str(price[0]) + " 溢价率：" + str(price[1]) + "\n"
            print s
            message = MIMEText((s), "plain", "utf-8")

            message["Subject"] = "quant 溢价超过1.8个点 交易机会"
            message["To"] = EMAIL_FROM
            message["From"] = EMAIL_FROM
        try:
            smtp = smtplib.SMTP_SSL(SMTP, 465)
            smtp.login(EMAIL_FROM, EMAIL_FROM_PASS)

            for email in EMAIL_TO:
                if message !="":
                    # print message
                    smtp.sendmail(EMAIL_FROM, email, message.as_string())
        except:
            print "email connect failed"

        # 持仓状态
        dictPriceDifference = futureCoinInformation(futureAPI,accountsAPI,dictRealizedFutureCoin,dictAvailableFutureCoin,dictPriceDifference,futureMaxDate)


        needCoin = {}
        for priceDifference in dictPriceDifference:
            if dictPriceDifference[priceDifference] < 100:
                needCoin[priceDifference] = dictPriceDifference[priceDifference]

        print dictPriceDifference
        count = count + 1
        time.sleep(30)

        smtp.quit()
        db.close()
