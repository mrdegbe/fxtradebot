import MetaTrader5 as mt5
import time

from core.analysis.structure.engine import StructureEngine
from core.analysis.topdown.engine import TopDownEngine
from core.data.mt5 import connect, shutdown, get_data
from core.models.setup import Setup
from core.setup.engine import SetupEvaluator
from infrastructure.telegram.alerts import send_telegram_message
from utils.helper import PAIRS

# Confidence threshold for alerts
CONFIDENCE_THRESHOLD = 20.0


def main():
    if not connect():
        return

    structure_engines = {pair: StructureEngine(pair) for pair in PAIRS}
    evaluator = {pair: SetupEvaluator(pair) for pair in PAIRS}

    try:
        while True:
            for symbol in PAIRS:
                # -------------------------------
                # 1️⃣ Fetch latest data
                # -------------------------------
                weekly_df = get_data(symbol, mt5.TIMEFRAME_W1)
                daily_df = get_data(symbol, mt5.TIMEFRAME_D1)
                h4_df = get_data(symbol, mt5.TIMEFRAME_H4)
                m15_df = get_data(symbol, mt5.TIMEFRAME_M15)

                if any(df is None for df in [weekly_df, daily_df, h4_df, m15_df]):
                    print(f"[{symbol}] Failed to fetch data, skipping...")
                    continue

                # -------------------------------
                # 2️⃣ Top-down analysis
                # -------------------------------
                topdown = TopDownEngine(symbol)
                snapshot = topdown.analyze(
                    {"W1": weekly_df, "D1": daily_df, "H4": h4_df, "M15": m15_df}
                )

                # -------------------------------
                # 3️⃣ Structure analysis
                # -------------------------------
                h4_snapshot = structure_engines[symbol].analyze(h4_df, timeframe="H4")
                m15_snapshot = structure_engines[symbol].analyze(
                    m15_df, timeframe="M15"
                )

                # -------------------------------
                # 4️⃣ Evaluate setup
                # -------------------------------
                setup: Setup | None = evaluator[symbol].evaluate(
                    snapshot, h4_snapshot, m15_snapshot, m15_df
                )
                print(f"[{symbol}] Evaluated setup: {setup}")

                # -------------------------------
                # 5️⃣ Send Telegram alert if valid
                # -------------------------------
                if setup and setup.confidence_score >= CONFIDENCE_THRESHOLD:
                    msg = (
                        f"PASIE Setup Detected!\n"
                        f"Pair: {setup.symbol}\n"
                        f"Direction: {setup.direction}\n"
                        f"Entry: {setup.entry:.5f}\n"
                        f"SL: {setup.stop_loss:.5f}\n"
                        f"TP: {setup.take_profit:.5f}\n"
                        f"RR: {setup.risk_reward:.2f}\n"
                        f"Confidence: {setup.confidence_score:.1f}"
                    )
                    print(msg)
                    send_telegram_message(msg)
                    
            # -------------------------------
            # 6️⃣ Wait for next M15 bar (~900s)
            # -------------------------------
            time.sleep(900)

    except KeyboardInterrupt:
        print("Stopping PASIE scanner...")

    finally:
        shutdown()


if __name__ == "__main__":
    main()
