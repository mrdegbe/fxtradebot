from core.analysis.structure.momentum import calculate_momentum
from core.analysis.structure.swings import strict_alternation_structure
from core.analysis.structure.swings import find_swings
from core.analysis.structure.bias import get_bias
from core.analysis.structure.bos import detect_bos
from core.analysis.structure.compression import compress_structure_after_bos


# ===================================================
# 6️⃣ MASTER STRUCTURE ENGINE (MULTI-PAIR SAFE)
# ===================================================


def analyze_structure(
    data,
    internal_lookback: int = 3,
    external_lookback: int = 7,
    tolerance: float = 0.00005,
    symbol: str | None = None,
):
    """
    Multi-pair market structure analyzer.
    Maintains persistent structural bias per symbol.
    """

    # ---------------------------------------------------
    # Validate symbol (required for multi-pair state)
    # ---------------------------------------------------
    if symbol is None:
        raise ValueError("Symbol must be provided for multi-pair structure tracking.")

    # ---------------------------------------------------
    # Initialize persistent state container
    # ---------------------------------------------------
    if not hasattr(analyze_structure, "_state"):
        analyze_structure._state = {}

    # Create symbol state if not existing
    if symbol not in analyze_structure._state:
        analyze_structure._state[symbol] = {
            "bias": None,
            "pending_bos": None,
            "pending_level": None,
            "awaiting_pullback": False,
        }

    state_memory = analyze_structure._state[symbol]

    # ---------------------------------------------------
    # External (macro) structure
    # ---------------------------------------------------
    external_swings = strict_alternation_structure(
        find_swings(data, external_lookback, tolerance)
    )

    # ---------------------------------------------------
    # Internal (micro) structure
    # ---------------------------------------------------
    internal_swings = strict_alternation_structure(
        find_swings(data, internal_lookback, tolerance)
    )

    internal_direction = get_bias(internal_swings)

    # ---------------------------------------------------
    # Detect Break of Structure (BOS)
    # ---------------------------------------------------
    bos = detect_bos(symbol, data, internal_swings)

    if bos:
        internal_swings = compress_structure_after_bos(internal_swings, bos)

    momentum = calculate_momentum(internal_swings)

    # ---------------------------------------------------
    # Structural baseline direction
    # ---------------------------------------------------
    structural_direction = get_bias(external_swings)

    # Initialize bias first time only
    if state_memory["bias"] is None:
        state_memory["bias"] = structural_direction

    # ---------------------------------------------------
    # Register BOS (but do not flip bias yet)
    # ---------------------------------------------------
    if bos:
        state_memory.update(
            {
                "pending_bos": bos["type"],
                "pending_level": bos["level"],
                "awaiting_pullback": True,
            }
        )

    # ---------------------------------------------------
    # Pullback confirmation logic
    # ---------------------------------------------------
    if state_memory["awaiting_pullback"]:

        last_close = data["Close"].iloc[-2]
        pending_type = state_memory["pending_bos"]
        pending_level = state_memory["pending_level"]

        # Bullish confirmation
        if (
            pending_type == "bullish_bos"
            and internal_direction == "bearish"
            and last_close > pending_level
        ):
            state_memory.update(
                {
                    "bias": "bullish",
                    "pending_bos": None,
                    "pending_level": None,
                    "awaiting_pullback": False,
                }
            )

        # Bearish confirmation
        elif (
            pending_type == "bearish_bos"
            and internal_direction == "bullish"
            and last_close < pending_level
        ):
            state_memory.update(
                {
                    "bias": "bearish",
                    "pending_bos": None,
                    "pending_level": None,
                    "awaiting_pullback": False,
                }
            )

    external_direction = state_memory["bias"]

    # ---------------------------------------------------
    # Structural state classification
    # ---------------------------------------------------
    state = "distribution"

    if external_direction == "bullish":
        if bos and bos["type"] == "bullish_bos":
            state = "bullish_expansion"
        elif internal_direction == "bearish":
            state = "bullish_correction"
        else:
            state = "bullish_expansion"

    elif external_direction == "bearish":
        if bos and bos["type"] == "bearish_bos":
            state = "bearish_expansion"
        elif internal_direction == "bullish":
            state = "bearish_correction"
        else:
            state = "bearish_expansion"

    else:
        state = "transition" if internal_direction != "neutral" else "distribution"

    return {
        "symbol": symbol,
        "external_direction": external_direction,
        "internal_direction": internal_direction,
        "state": state,
        "bos": bos,
        "momentum_score": momentum,
        "external_swings": external_swings,
        "internal_swings": internal_swings,
    }
