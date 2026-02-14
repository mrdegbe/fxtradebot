import MetaTrader5 as mt5


def connect():
    if not mt5.initialize():
        print("Initialization failed:", mt5.last_error())
        return False

    print("MT5 connected")
    return True


def shutdown():
    mt5.shutdown()
