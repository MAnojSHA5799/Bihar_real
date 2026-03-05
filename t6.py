# =========================================================
# t6.py → ADVANCED DYNAMIC FORECAST MODEL
# =========================================================

import random

def sales_category(prob):
    if prob >= 80:
        return "High Sales Growth Expected"
    elif prob >= 60:
        return "Moderate Stable Sales"
    elif prob >= 40:
        return "Sales Risk Zone"
    else:
        return "High Sales Decline Risk"


def growth_indicator(trust, risk):
    if trust > 50 and risk < 5:
        return "Strong Positive Growth Trend"
    elif trust > 30:
        return "Stable but Improvement Needed"
    else:
        return "Critical Risk – Immediate Strategy Required"


def dynamic_growth(trust, risk):
    """
    Growth trust se increase hoti hai
    Risk se reduce hoti hai
    Random market momentum factor bhi add
    """

    base_growth = 0.05   # 5% base

    trust_bonus = trust / 100 * 0.08   # up to 8% bonus
    risk_penalty = risk * 0.01         # 1% per risk issue
    market_momentum = random.uniform(-0.01, 0.02)  # -1% to +2%

    growth_1yr = base_growth + trust_bonus - risk_penalty + market_momentum

    # Ensure negative extreme avoid
    if growth_1yr < 0:
        growth_1yr = 0.01

    # 2 year compounded
    growth_2yr = (1 + growth_1yr) ** 2 - 1

    return round(growth_1yr, 3), round(growth_2yr, 3)


def nearby_development(trust):

    if trust > 60:
        return "Mall, school, hospital, transport expansion expected."

    elif trust > 40:
        return "Retail shops, local markets, road improvement likely."

    else:
        return "Slow development until project credibility improves."


# =========================================================
# MAIN APPLY FUNCTION
# =========================================================

def apply_prediction(summary_df):

    summary_df["Predicted Sales Category"] = summary_df["Sales Probability (%)"].apply(sales_category)

    summary_df["Performance Trend"] = summary_df.apply(
        lambda row: growth_indicator(
            row["Trust Score (0-100)"],
            row["Risk Score"]
        ), axis=1
    )

    # 🔥 Each promoter different base price
    summary_df["Base Price"] = [
        random.randint(4500000, 6500000)
        for _ in range(len(summary_df))
    ]

    # Dynamic growth
    growth_values = summary_df.apply(
        lambda row: dynamic_growth(
            row["Trust Score (0-100)"],
            row["Risk Score"]
        ), axis=1
    )

    summary_df["1 Year Growth %"] = [g[0] for g in growth_values]
    summary_df["2 Year Growth %"] = [g[1] for g in growth_values]

    # Compounded price
    summary_df["Projected Price After 1 Year"] = summary_df["Base Price"] * (1 + summary_df["1 Year Growth %"])
    summary_df["Projected Price After 2 Years"] = summary_df["Base Price"] * (1 + summary_df["2 Year Growth %"])

    summary_df["Expected Nearby Development"] = summary_df["Trust Score (0-100)"].apply(nearby_development)

    return summary_df