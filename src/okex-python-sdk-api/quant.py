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

    api_key = '42ab348f-14aa-4754-ad0e-bd3f05f5a03b'
    seceret_key = 'FD2BCD95A08F9E6FA7ED9BD83D61B513'
    passphrase = '123.fighting'
    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
    swapAPI = swap.SwapAPI(api_key, seceret_key, passphrase, True)


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

        endPriceList = {}
        for price in  priceList:
            if price[1]>=0.023 :
                endPriceList[price[0]]=price[1]
        endPriceList = sorted(endPriceList.items(), key=lambda d: d[1], reverse=True)

        if endPriceList:
            s = ""
            for price in endPriceList:
                s = s +"币种："+str(price[0])+ " 溢价率："+str(price[1])+"\n"
            print s
            message = MIMEText((s), "plain", "utf-8")

            message["Subject"] = "quant交易机会"
            message["To"] = "1158362548@qq.com"
            message["From"] = "1158362548@qq.com"

            smtp = smtplib.SMTP_SSL("smtp.qq.com",465)  # 465或587是一个固定值，smtp服务器端口号

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
        time.sleep(103)

