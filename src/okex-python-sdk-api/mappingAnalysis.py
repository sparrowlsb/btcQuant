#coding=utf-8
import matplotlib.pyplot as plt#约定俗成的写法plt
import numpy as np
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
if __name__ == '__main__':
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DBNAME)

    time = distinctTime(db)
    print time
    results = premiumAnalysis(db)

    print len(time)
    EOSPremium = []
    ETHPremium = []
    LTCPremium = []
    BCHPremium = []
    XRPPremium = []
    BTCPremium = []
    BSVPremium = []
    ETCPremium = []

    for data in results:
        if "EOS-USD" == data[1]:
            EOSPremium.append(data[2]*100)
        elif "ETH-USD" == data[1]:
            ETHPremium.append(data[2]*100)
        elif "LTC-USD" == data[1]:
            LTCPremium.append(data[2]*100)
        elif "BCH-USD" == data[1]:
            BCHPremium.append(data[2]*100)
        elif "XRP-USD" == data[1]:
            XRPPremium.append(data[2]*100)
        elif "BTC-USD" == data[1]:
            BTCPremium.append(data[2]*100)
        elif "BSV-USD" == data[1]:
            BSVPremium.append(data[2]*100)
        elif "ETC-USD" == data[1]:
            ETCPremium.append(data[2]*100)

    x = time  # X轴数据
    y1 = EOSPremium  # Y轴数据
    y2 = ETHPremium  # Y轴数据
    y3 = LTCPremium  # Y轴数据
    y4 = BCHPremium  # Y轴数据
    y5 = XRPPremium  # Y轴数据
    y6 = BTCPremium  # Y轴数据
    y7 = BSVPremium  # Y轴数据
    y8 = ETCPremium  # Y轴数据

    plt.figure(figsize=(16, 6))
    plt.subplot(4, 2, 1)
    plt.plot(x, y1, label="EOS-Premium", color="red", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium EOS Quant")

    plt.subplot(4, 2, 2)
    plt.plot(x, y2, label="ETH-Premium", color="blue", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium ETH Quant")

    plt.subplot(4, 2, 3)
    plt.plot(x, y3, label="LTC-Premium", color="#f45324", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium LTC Quant")

    plt.subplot(4, 2, 4)
    plt.plot(x, y4, label="BCH-Premium", color="#340000", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium BCH Quant")

    plt.subplot(4, 2, 5)
    plt.plot(x, y5, label="XRP-Premium", color="#123312", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium XRP Quant")

    plt.subplot(4, 2, 6)
    plt.plot(x, y6, label="BTC-Premium", color="#243242", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium BTC Quant")

    plt.subplot(4, 2, 7)
    plt.plot(x, y7, label="BSV-Premium", color="#435234", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium BSV Quant")

    plt.subplot(4, 2, 8)
    plt.plot(x, y8, label="ETC-Premium", color="#867567", linewidth=1)
    plt.xlabel("Time(s)")
    plt.ylabel("Premium(%)")
    plt.title("Premium ETC Quant")

    # 指定曲线的颜色和线性，如‘b--’表示蓝色虚线（b：蓝色，-：虚线）



    '''
    使用关键字参数可以指定所绘制的曲线的各种属性：
    label：给曲线指定一个标签名称，此标签将在图标中显示。如果标签字符串的前后都有字符'$'，则Matplotlib会使用其内嵌的LaTex引擎将其显示为数学公式
    color：指定曲线的颜色。颜色可以用如下方法表示
           英文单词
           以‘#’字符开头的3个16进制数，如‘#ff0000’表示红色。
           以0~1的RGB表示，如（1.0,0.0,0.0）也表示红色。
    linewidth：指定权限的宽度，可以不是整数，也可以使用缩写形式的参数名lw。
    '''

    plt.ylim(-0.04*100, 0.04*100)
    plt.legend()  # 显示左下角的图例

    plt.show()