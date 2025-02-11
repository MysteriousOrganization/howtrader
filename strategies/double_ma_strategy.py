from howtrader.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData,
    BarGenerator,
    ArrayManager,
)

import pandas_ta as ta
import pandas as pd
from datetime import datetime, timedelta
import pytz
utc=pytz.UTC


class DoubleMaStrategy(CtaTemplate):
    fast_window = 5
    slow_window = 10

    fast_ma0 = 0.0
    fast_ma1 = 0.0

    slow_ma0 = 0.0
    slow_ma1 = 0.0

    parameters = ["fast_window", "slow_window"]
    variables = ["fast_ma0", "fast_ma1", "slow_ma0", "slow_ma1"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")
        self.load_bar(1)

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

        self.put_event()

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        """
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        am = self.am
        am.update_bar(bar)
        if not am.inited:
            return

        self.write_log("bar.datetime:{}".format(bar.datetime))
        now = datetime.now()
        now = now.replace(tzinfo=bar.datetime.tzinfo)
        if bar.datetime + timedelta(seconds=120) < now:
            return

        close = pd.Series(am.close_array)
        fast_ma = ta.sma(close, self.fast_window)
        self.fast_ma0 = fast_ma.iloc[-1]
        self.fast_ma1 = fast_ma.iloc[-2]

        slow_ma = ta.sma(close, self.slow_window)
        self.slow_ma0 = slow_ma.iloc[-1]
        self.slow_ma1 = slow_ma.iloc[-2]

        cross_over = self.fast_ma0 > self.slow_ma0 and self.fast_ma1 < self.slow_ma1
        cross_below = self.fast_ma0 < self.slow_ma0 and self.fast_ma1 > self.slow_ma1

        print("self.pos:{}".format(self.pos))
        if cross_over:
            if self.pos == 0:
                self.buy(bar.close_price, 20/bar.close_price)
            elif self.pos < 0:
                self.cover(bar.close_price, 20/bar.close_price)
                self.buy(bar.close_price, 20/bar.close_price)

        elif cross_below:
            if self.pos == 0:
                self.short(bar.close_price, 20/bar.close_price)
            elif self.pos > 0:
                self.sell(bar.close_price, 20/bar.close_price)
                self.short(bar.close_price, 20/bar.close_price)

        self.put_event()

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        pass

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        pass
