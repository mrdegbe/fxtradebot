# analysis/mtf/topdown_engine.py

from typing import Dict
from core.analysis.structure.structure_engine import analyze_structure
from core.analysis.mtf.timeframe_map import TIMEFRAMES
from core.market_data.data_fetcher import get_data


class TopDownEngine:

    def __init__(self, get_data_function):
        """
        get_data_function must implement:
            get_data(symbol: str, timeframe_code: str) -> DataFrame
        """
        self.get_data_function = get_data_function

    def analyze_symbol(self, symbol: str) -> Dict[str, object]:
        """
        Runs structure analysis across all configured timeframes.
        Returns dictionary of StructureSnapshot per timeframe.
        """

        snapshots = {}

        # Process highest → lowest timeframe
        ordered_timeframes = sorted(
            TIMEFRAMES.values(), key=lambda tf: tf.rank, reverse=True
        )

        for tf in ordered_timeframes:

            data = self.get_data_function(symbol, tf.code)

            snapshot = analyze_structure(data=data, symbol=symbol)

            # Inject timeframe label
            snapshot.timeframe = tf.name

            snapshots[tf.name] = snapshot

        return snapshots
