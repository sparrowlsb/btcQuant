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
from okex.consts import *
from okex.premium import *
if __name__ == '__main__':

    api_key = API_KEY
    seceret_key = SECERET_KEY
    passphrase = PASSPARASE
    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
    swapAPI = swap.SwapAPI(api_key, seceret_key, passphrase, True)
    smtp = smtplib.SMTP_SSL(SMTP, 465)

    count = 0
    while True:
        # future api test
        dictRealizedFutureCoin = {}
        dictAvailableFutureCoin = {}
        dictPriceDifference = {}

        accountsAPI = futureAPI.get_accounts()

        futureResultTicker = futureAPI.get_ticker()
        swapResultTicker = swapAPI.get_ticker()
        # 合约季度时间
        futureMaxDate = maxDateFuture(futureResultTicker)
        # 溢价排序
        priceList = {}
        priceList = premiumInformation(futureResultTicker,swapResultTicker,futureMaxDate)
        print priceList

        endLowPriceList = {}
        endMidPriceList = {}
        endGoodPriceList = {}
        endWonderPriceList = {}

        for price in  priceList:
            if price[1]>=0.02 :
                endLowPriceList[price[0]]=price[1]
            if price[1] >= 0.23:
                endMidPriceList[price[0]] = price[1]
            if price[1] >= 0.03:
                endGoodPriceList[price[0]] = price[1]
            if price[1] >= 0.05:
                endWonderPriceList[price[0]] = price[1]

        endLowPriceList = sorted(endLowPriceList.items(), key=lambda d: d[1], reverse=True)
        endMidPriceList = sorted(endMidPriceList.items(), key=lambda d: d[1], reverse=True)
        endGoodPriceList = sorted(endGoodPriceList.items(), key=lambda d: d[1], reverse=True)
        endWonderPriceList = sorted(endWonderPriceList.items(), key=lambda d: d[1], reverse=True)

        if endLowPriceList and count%20 == 0:
            s = ""
            for price in endLowPriceList:
                s = s +"币种："+str(price[0])+ " 溢价率："+str(price[1])+"\n"
            print s
            message = MIMEText((s), "plain", "utf-8")

            message["Subject"] = "quant交易机会"
            message["To"] = "1158362548@qq.com"
            message["From"] = "1158362548@qq.com"


            smtp.login("a1158362548@qq.com", "zhzxprpjgtiwfedh")
            smtp.sendmail("a1158362548@qq.com", ["a1158362548@qq.com"], message.as_string())
            smtp.sendmail("a1158362548@qq.com", ["464147349@qq.com"], message.as_string())

            smtp.quit()

        # 持仓状态
        dictPriceDifference = futureCoinInformation(futureAPI,accountsAPI,dictRealizedFutureCoin,dictAvailableFutureCoin,dictPriceDifference,futureMaxDate)


        needCoin = {}
        for priceDifference in dictPriceDifference:
            if dictPriceDifference[priceDifference] < 100:
                needCoin[priceDifference] = dictPriceDifference[priceDifference]

        print dictPriceDifference
        count = count + 1
        time.sleep(30)

