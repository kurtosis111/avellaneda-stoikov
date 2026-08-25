import math


def optimal_quotes(
    reservation: float,
    gamma: float,
    k: float,
) -> tuple[float, float]:
    """
    Calculate optimal ask and bid quotes.

    Half-spread:

        delta = (1/gamma) * log(1 + gamma/k)

    Quotes:

        ask = reservation + delta
        bid = reservation - delta
    """

    half_spread = (
        1.0 / gamma
        * math.log(1.0 + gamma / k)
    )

    ask = reservation + half_spread
    bid = reservation - half_spread

    return bid, ask