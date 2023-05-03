from typing import Dict
from datetime import datetime

from pandas import DataFrame

from freqtrade.constants import Config
from freqtrade.optimize.hyperopt import IHyperOptLoss


class WinPercentageHyperOptLoss(IHyperOptLoss):
    @staticmethod
    def hyperopt_loss_function(
        results: DataFrame, trade_count: int, min_date: datetime, max_date: datetime, config: Config, processed: Dict[str, DataFrame], *args, **kwargs
    ) -> float:
        """
        Objective function, returns smaller number for better _results
        """
        amount_of_trades = len(results)
        win_percentage = results["profit_ratio"].gt(0).sum() / amount_of_trades
        return -win_percentage
