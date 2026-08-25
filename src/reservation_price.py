def reservation_price(
    mid_price: float,
    inventory: float,
    gamma: float,
    sigma: float,
    time_remaining: float,
) -> float:
    """
    Avellaneda-Stoikov reservation price.

    r_t = S_t - q_t * gamma * sigma^2 * (T - t)
    """

    return (
        mid_price
        - inventory * gamma * sigma**2 * time_remaining
    )