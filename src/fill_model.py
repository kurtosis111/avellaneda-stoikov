import math
import random


def fill_probabilities(
    bid: float,
    ask: float,
    mid_price: float,
    A: float,
    k: float,
    dt: float,
) -> tuple[float, float]:
    """
    Calculate bid/ask fill probabilities.

    lambda(delta) = A * exp(-k * delta)

    P(fill during dt) = 1 - exp(-lambda * dt)
    """

    delta_bid = mid_price - bid
    delta_ask = ask - mid_price

    lambda_bid = A * math.exp(-k * delta_bid)
    lambda_ask = A * math.exp(-k * delta_ask)

    prob_bid = 1.0 - math.exp(-lambda_bid * dt)
    prob_ask = 1.0 - math.exp(-lambda_ask * dt)

    return prob_bid, prob_ask


def simulate_fills(
    prob_bid: float,
    prob_ask: float,
) -> tuple[int, int]:
    """
    Simulate whether bid and ask are filled.

    Returns
    -------
    bid_fill, ask_fill
    """

    bid_fill = int(random.random() < prob_bid)
    ask_fill = int(random.random() < prob_ask)

    return bid_fill, ask_fill