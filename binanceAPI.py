from binance.client import Client
from binance.enums import *
import time
import warnings
warnings.filterwarnings("ignore")

# Klines
class coin_Kline:
    def __init__(self,api_key,secret_key):
        self.client = Client(api_key,secret_key)

    def futures_Kline(self,startTime, endTime, interval=KLINE_INTERVAL_2HOUR):
        request = self.client.futures_coin_klines(
            symbol="BTCUSD_PERP",
            interval=interval,
            startTime=startTime,
            endTime=endTime,
            limit=1500
        )
        return request

    def get_AllKlines(self,interval,interval_ms, firstCandleTime = 1597118400000):
        START = time.time()
        klines_list = []
        timeLoop_list = []
        index = 0
        initialTime = firstCandleTime
        maxInterval = interval_ms * 1500 
        initialTime = initialTime - maxInterval
        while True:
            index += 1
            initialTime += maxInterval
            timeLoop_list.append(initialTime)
            if timeLoop_list[-1] + maxInterval < int(time.time() * 1000):
                requestTimeStart = time.time()
                klinesLoop = self.futures_Kline(timeLoop_list[index-1], timeLoop_list[index-1] + maxInterval, interval)
                klines_list.extend(klinesLoop)
                print("\nLoop : "+str(index))
                print("\nQtd  : "+str(len(klines_list)))
                requestTimeEnd = time.time()
                requestDuration = requestTimeEnd - requestTimeStart
                if requestDuration < 1.33:
                    time.sleep(1.33 - requestDuration)
            else:
                print("Else Reached!")
                lastCall = self.futures_Kline(timeLoop_list[-1] + 1, "", interval)
                klines_list.extend(lastCall)
                print("\nQtd  : "+str(len(klines_list)))
                print("\nLoop Finalizado\n")
                
                END = time.time()
                print("\nExecution time: "+str(END-START))
                break
        return klines_list

    def get_HistoricalKlines(self,interval,interval_ms, firstCandleTime = 1597118400000):
        START = time.time()
        klines_list = []
        timeLoop_list = []
        index = 0
        initialTime = firstCandleTime
        maxInterval = interval_ms * 1500 
        initialTime = initialTime - maxInterval
        while True:
            index += 1
            initialTime += maxInterval
            timeLoop_list.append(initialTime)
            if timeLoop_list[-1] + maxInterval < int(time.time() * 1000):
                requestTimeStart = time.time()
                klinesLoop = self.futures_Kline(timeLoop_list[index-1], timeLoop_list[index-1] + maxInterval, interval)
                klines_list.extend(klinesLoop)
                print("\nLoop : "+str(index))
                print("\nQtd  : "+str(len(klines_list)))
                requestTimeEnd = time.time()
                requestDuration = requestTimeEnd - requestTimeStart
                if requestDuration < 1.33:
                    time.sleep(1.33 - requestDuration)
            else:
                print("\nLoop Finalizado\n")
                
                END = time.time()
                print("\nExecution time: "+str(END-START))
                break
        return klines_list

    def markPrice_futures_Kline(self,startTime, endTime, interval=KLINE_INTERVAL_2HOUR):
        request = self.client.futures_coin_mark_price_klines(
            symbol="BTCUSD_PERP",
            interval=interval,
            startTime=startTime,
            endTime=endTime,
            limit=1500
        )
        return request

    def get_markPrice_AllKlines(self,interval,interval_ms, firstCandleTime = 1597118400000):
        START = time.time()
        kline_List = []
        timeLoop = []
        index = 0
        initialTime = firstCandleTime
        maxInterval = interval_ms * 1500 
        initialTime = initialTime - maxInterval
        while True:
            initialTime += maxInterval
            index += 1
            timeLoop.append(initialTime)
            if timeLoop[-1] + maxInterval < int(time.time() * 1000):
                requestTimeStart = time.time()
                klinesLoop = self.markPrice_futures_Kline(timeLoop[index-1], timeLoop[index-1] + maxInterval, interval)
                kline_List.extend(klinesLoop)
                print("\nLoop : "+str(index))
                print("\nQtd  : "+str(len(kline_List)))
                requestTimeEnd = time.time()
                requestDuration = requestTimeEnd - requestTimeStart
                if requestDuration < 1.33:
                    time.sleep(1.33 - requestDuration)
            else:
                print("Else Reached!")
                lastCall = self.markPrice_futures_Kline(timeLoop[-1] + 1, "", interval)
                kline_List.extend(lastCall)
                print("\nQtd  : "+str(len(kline_List)))
                print("\nLoop Finalizado\n")
                
                END = time.time()
                print("\nExecution time: "+str(END-START))
                break
        return kline_List

#Classe ainda não testada
class coin_Trade: 
    def __init__(self,api_key,secret_key):
        self.client = Client(api_key,secret_key)
    
    def get_open_orders(self):
        return self.client.futures_coin_get_open_orders()

    def get_all_orders(self):
        return self.client.futures_coin_get_all_orders(symbol='BTCUSD_PERP')

    def stopBuy(self,price,quantity):
        return self.client.futures_coin_create_order(symbol='BTCUSD_PERP',
        side='BUY',
        type='STOP_MARKET',
        stopPrice=price,
        quantity=quantity,
        )

    def stopMarket(self,stopPrice):
        # Stop Market
        return self.client.futures_coin_create_order(symbol='BTCUSD_PERP',
        side='SELL',
        type='STOP_MARKET',
        stopPrice=stopPrice,
        closePosition='true',
        priceProtect='TRUE',
        )

    def buyMarket(self,quantity):
        # buy at Market Price
        return self.client.futures_coin_create_order(symbol='BTCUSD_PERP',
        side='BUY',
        type='MARKET',
        quantity=quantity,
        )

    def takeProfit(self,takeProfit):
        # Take Profit
        return self.client.futures_create_order(symbol='BTCUSD_PERP',
        side='SELL',
        type='LIMIT',
        timeInForce='GTC',
        stopPrice=takeProfit,
        closePosition='true',
        priceProtect='TRUE',
        )

    def buyPosition(self,contracts,entryPrice,profitPrice,stopPrice):
        entry = {
            'symbol':'BTCUSD_PERP',
            'side':'BUY',
            'type':'STOP_MARKET',
            'stopPrice':str(entryPrice),
            'quantity':str(contracts)
        }

        takeProfit = {
            'symbol':'BTCUSD_PERP',
            'side':'SELL',
            'type':'TAKE_PROFIT_MARKET',
            'stopPrice':str(profitPrice),
            'closePosition':'True',
        }

        stopLoss = {
            'symbol':'BTCUSD_PERP',
            'side':'SELL',
            'type':'STOP_MARKET',
            'stopPrice':str(stopPrice),
            'closePosition':'True'
        }

        PositionOrder = []
        PositionOrder.append(entry)
        PositionOrder.append(takeProfit)
        PositionOrder.append(stopLoss)
        return  self.client.futures_coin_place_batch_order(batchOrders=PositionOrder)

    def sellPosition(self,contracts,entryPrice,profitPrice,stopPrice):
        entry = {
            'symbol':'BTCUSD_PERP',
            'side':'SELL',
            'type':'STOP_MARKET',
            'stopPrice':str(entryPrice),
            'quantity':str(contracts)
        }

        takeProfit = {
            'symbol':'BTCUSD_PERP',
            'side':'BUY',
            'type':'TAKE_PROFIT_MARKET',
            'stopPrice':str(profitPrice),
            'closePosition':'True',
        }

        stopLoss = {
            'symbol':'BTCUSD_PERP',
            'side':'BUY',
            'type':'STOP_MARKET',
            'stopPrice':str(stopPrice),
            'closePosition':'True'
        }

        PositionOrder = []
        PositionOrder.append(entry)
        PositionOrder.append(takeProfit)
        PositionOrder.append(stopLoss)
        return self.client.futures_coin_place_batch_order(batchOrders=PositionOrder)

    def TakeProfitMarket(self,price):
        self.client.futures_coin_create_order(symbol='BTCUSD_PERP',
        side='SELL',
        type='TAKE_PROFIT_MARKET',
        stopPrice=price,
        closePosition='true',
        priceProtect='TRUE',
        )

    def Limit(self,price):
        return self.client.futures_coin_create_order(symbol='BTCUSD_PERP',
        side='SELL',
        type='LIMIT',
        stopPrice=price,
        closePosition='true',
        priceProtect='TRUE',
        )

    def StopLimit(self,price,stopPrice):
        return self.client.futures_coin_create_order(symbol='BTCUSD_PERP',
        side='SELL',
        type='STOP',
        stopPrice=stopPrice,
        price=price,
        closePosition='true',
        priceProtect='TRUE',
        )

    def cancelAllOrders(self,symbol='BTCUSD_PERP'):
        return self.client.futures_coin_cancel_all_open_orders(symbol=symbol)
    
    def leverage(self,leverage,symbol='BTCUSD_PERP'):
        leverageRequest = self.client.futures_coin_change_leverage(
        symbol=symbol,
        leverage=leverage,
        )
        print("Leverage changed to: "+str(leverage))
        return leverageRequest
    def maxLeverage(self,tradeRisk,symbol='BTCUSD_PERP'):
        maxLeverage = round(1 / tradeRisk * 0.65)
        maxLeverageRequest = self.client.futures_coin_change_leverage(
        symbol=symbol,
        leverage=maxLeverage,
        )
        print("Leverage changed to: "+str(maxLeverage))
        return maxLeverageRequest
    def positionInfo(self):
        return self.client.futures_coin_position_information()