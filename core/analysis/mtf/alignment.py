def determine_overall_bias(weekly, daily, h4):

    if weekly.direction == daily.direction and daily.direction == h4.direction:
        return weekly.direction

    # Potential reversal zone
    if weekly.direction != daily.direction:
        return "reversal_watch"

    return "neutral"


alignment = 0

# if weekly.direction == daily.direction:
#     alignment += 1

# if daily.direction == h4.direction:
#     alignment += 1

# if h4.direction == "neutral":
#     alignment += 1
