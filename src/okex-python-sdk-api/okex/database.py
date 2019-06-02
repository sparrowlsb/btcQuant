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

def premiumInsert(db,priceList,timestamp):
    cursor = db.cursor()

    for price in priceList:
        # SQL 插入语句
        sql = 'insert into premium_information(coin_name,premium_price,premium_data) values(\'%s\',\'%s\' ,\'%s\')' % (price, priceList[price],timestamp['timestamp'])
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

def gettingPremiumSTD(db):
    cursor = db.cursor()

    # SQL 插入语句
    sql = 'select  coin_name ,STD(`premium_price`) from premium_information WHERE DATEDIFF(`premium_data`,NOW())<0 AND DATEDIFF(premium_data,NOW())>=-2 group by coin_name order by STD(`premium_price`) desc  limit 3'

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


def gettingPremiumAVGPositive(db):
    cursor = db.cursor()

    # SQL 插入语句 查找12小时的值
    sql = 'select  coin_name ,(max(`premium_price`)-avg(`premium_price`))/1.5+avg(`premium_price`) as avg from premium_information WHERE unix_timestamp(premium_data)>=unix_timestamp(now())-43200 group by coin_name order by STD(`premium_price`) desc '

    # premiumCoinList['']
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        # Rollback in case there is any error
        print 'gettingPremiumAVGPositive error'
        db.rollback()


def gettingPremiumAVGNegative(db):
    cursor = db.cursor()

    # SQL 插入语句 查找12小时的值
    sql = 'select  coin_name ,(max(`premium_price`)-avg(`premium_price`))/1.5+avg(`premium_price`) from premium_information WHERE unix_timestamp(premium_data)>=unix_timestamp(now())-43200 group by coin_name order by STD(`premium_price`) desc '

    # premiumCoinList['']
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except:
        # Rollback in case there is any error
        print 'gettingPremiumAVGNegative error'
        db.rollback()