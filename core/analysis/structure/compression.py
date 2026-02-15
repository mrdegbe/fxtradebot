
def compress_structure_after_bos(swings, bos):
    """
    Compress swing structure after confirmed BOS.

    Keeps:
    - The protected swing level (last opposite swing before BOS)
    - The newest swing that confirms the new structure
    """

    # ---------------------------------------------------
    # Guard Clauses
    # ---------------------------------------------------
    if bos is None or len(swings) < 2:
        return swings

    bos_level = bos["level"]
    bos_type = bos["type"]

    # ---------------------------------------------------
    # Locate the swing level that was broken
    # ---------------------------------------------------
    broken_index = next(
        (i for i, s in enumerate(swings) if abs(s[1] - bos_level) < 1e-10),
        None,
    )

    if broken_index is None:
        return swings

    # ---------------------------------------------------
    # Bullish BOS → find last LOW before broken HIGH
    # ---------------------------------------------------
    if bos_type == "bullish_bos":
        for i in range(broken_index - 1, -1, -1):
            if swings[i][2] == "low":
                return [swings[i], swings[-1]]

    # ---------------------------------------------------
    # Bearish BOS → find last HIGH before broken LOW
    # ---------------------------------------------------
    if bos_type == "bearish_bos":
        for i in range(broken_index - 1, -1, -1):
            if swings[i][2] == "high":
                return [swings[i], swings[-1]]

    return swings
