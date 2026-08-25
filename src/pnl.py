def update_inventory(
    inventory: float,
    bid_fill: int,
    ask_fill: int,
) -> float:
    """
    Inventory update:

        dq = dN_bid - dN_ask
    """

    return inventory + bid_fill - ask_fill


def update_cash(
    cash: float,
    bid: float,
    ask: float,
    bid_fill: int,
    ask_fill: int,
) -> float:
    """
    Cash update:

        dX = ask * dN_ask - bid * dN_bid
    """

    return (
        cash
        + ask * ask_fill
        - bid * bid_fill
    )


def mark_to_market(
    cash: float,
    inventory: float,
    mid_price: float,
) -> float:
    """
    Total wealth:

        W = X + qS
    """

    return cash + inventory * mid_price