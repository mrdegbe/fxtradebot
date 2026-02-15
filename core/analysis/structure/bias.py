import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

Swing = Tuple  # (timestamp, price, type)


def get_bias(swings: List[Swing], tolerance: float = 0.0) -> str:
    """
    Determine market structural direction using sequential swing logic.

    Parameters
    ----------
    swings : List[Tuple]
        List of swings formatted as (timestamp, price, type),
        where type is either "high" or "low".

    tolerance : float
        Allowed tolerance when comparing swing prices.
        Helps ignore tiny price differences caused by noise.

    Returns
    -------
    str
        "bullish", "bearish", or "neutral"
    """

    if len(swings) < 4:
        logger.debug("Not enough swings to determine direction.")
        return "neutral"

    # Extract last 4 swings (latest structural cycle)
    s1, s2, s3, s4 = swings[-4:]

    logger.debug("Evaluating swings: %s", [s1, s2, s3, s4])

    # -----------------------------------------
    # Pattern: High → Low → High → Low
    # -----------------------------------------
    if s1[2] == "high" and s2[2] == "low" and s3[2] == "high" and s4[2] == "low":

        prev_high, prev_low = s1[1], s2[1]
        last_high, last_low = s3[1], s4[1]

        if last_high > prev_high * (1 - tolerance) and last_low > prev_low * (
            1 - tolerance
        ):
            logger.info("Structure identified as BULLISH.")
            return "bullish"

        if last_high < prev_high * (1 + tolerance) and last_low < prev_low * (
            1 + tolerance
        ):
            logger.info("Structure identified as BEARISH.")
            return "bearish"

    # -----------------------------------------
    # Pattern: Low → High → Low → High
    # -----------------------------------------
    elif s1[2] == "low" and s2[2] == "high" and s3[2] == "low" and s4[2] == "high":

        prev_low, prev_high = s1[1], s2[1]
        last_low, last_high = s3[1], s4[1]

        if last_high > prev_high * (1 - tolerance) and last_low > prev_low * (
            1 - tolerance
        ):
            logger.info("Structure identified as BULLISH.")
            return "bullish"

        if last_high < prev_high * (1 + tolerance) and last_low < prev_low * (
            1 + tolerance
        ):
            logger.info("Structure identified as BEARISH.")
            return "bearish"

    logger.debug("No clear structure detected.")
    return "neutral"
