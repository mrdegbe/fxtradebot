import MetaTrader5 as mt5
import logging

logger = logging.getLogger(__name__)


def connect() -> bool:
    """
    Initialize connection to MetaTrader5 terminal.

    Returns:
        True if connection successful, otherwise False.
    """
    if mt5.initialize():
        logger.info("MT5 connected")
        return True

    logger.error(f"MT5 initialization failed: {mt5.last_error()}")
    return False


def shutdown() -> None:
    """
    Shutdown MetaTrader5 connection safely.
    """
    if mt5.initialize():
        mt5.shutdown()
        logger.info("MT5 connection closed")
