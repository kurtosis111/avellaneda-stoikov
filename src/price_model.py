import numpy as np


def brownian_price(
    s0: float,
    sigma: float,
    T: float,
    N: int,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Simulate a Brownian-motion mid-price.

    dS_t = sigma * dW_t

    Returns
    -------
    t : time grid
    s : simulated mid-price
    """

    rng = np.random.default_rng(seed)

    dt = T / N
    t = np.linspace(0.0, T, N + 1)

    shocks = rng.normal(
        loc=0.0,
        scale=sigma * np.sqrt(dt),
        size=N,
    )

    s = np.empty(N + 1)
    s[0] = s0
    s[1:] = s0 + np.cumsum(shocks)

    return t, s