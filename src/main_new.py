import numpy as np
import matplotlib.pyplot as plt

from price_model import brownian_price
from reservation_price import reservation_price
from optimal_quotes import optimal_quotes
from fill_model import fill_probabilities, simulate_fills
from pnl import (
    update_inventory,
    update_cash,
    mark_to_market,
)


# ============================================================
# Parameters
# ============================================================

S0 = 100.0
sigma = 4.0
T = 0.5
N = 200

gamma = 0.1
k = 1.5

A = 100.0

seed = 42


# ============================================================
# Price model
# ============================================================

t, s = brownian_price(
    s0=S0,
    sigma=sigma,
    T=T,
    N=N,
    seed=seed,
)

dt = T / N


# ============================================================
# State variables
# ============================================================

inventory = np.zeros(N + 1)
cash = np.zeros(N + 1)
pnl = np.zeros(N + 1)

reservation = np.zeros(N + 1)
bid = np.zeros(N + 1)
ask = np.zeros(N + 1)

prob_bid = np.zeros(N)
prob_ask = np.zeros(N)


# ============================================================
# Market-making loop
# ============================================================

for n in range(N):

    # --------------------------------------------------------
    # 1. Reservation price
    # --------------------------------------------------------

    time_remaining = T - t[n]

    reservation[n] = reservation_price(
        mid_price=s[n],
        inventory=inventory[n],
        gamma=gamma,
        sigma=sigma,
        time_remaining=time_remaining,
    )

    # --------------------------------------------------------
    # 2. Optimal quotes
    # --------------------------------------------------------

    bid[n], ask[n] = optimal_quotes(
        reservation=reservation[n],
        gamma=gamma,
        k=k,
    )

    # --------------------------------------------------------
    # 3. Fill probabilities
    # --------------------------------------------------------

    prob_bid[n], prob_ask[n] = fill_probabilities(
        bid=bid[n],
        ask=ask[n],
        mid_price=s[n],
        A=A,
        k=k,
        dt=dt,
    )

    # --------------------------------------------------------
    # 4. Simulate execution
    # --------------------------------------------------------

    bid_fill, ask_fill = simulate_fills(
        prob_bid=prob_bid[n],
        prob_ask=prob_ask[n],
    )

    # --------------------------------------------------------
    # 5. Update inventory
    # --------------------------------------------------------

    inventory[n + 1] = update_inventory(
        inventory=inventory[n],
        bid_fill=bid_fill,
        ask_fill=ask_fill,
    )

    # --------------------------------------------------------
    # 6. Update cash
    # --------------------------------------------------------

    cash[n + 1] = update_cash(
        cash=cash[n],
        bid=bid[n],
        ask=ask[n],
        bid_fill=bid_fill,
        ask_fill=ask_fill,
    )

    # --------------------------------------------------------
    # 7. Mark-to-market P&L
    # --------------------------------------------------------

    pnl[n + 1] = mark_to_market(
        cash=cash[n + 1],
        inventory=inventory[n + 1],
        mid_price=s[n],
    )


# Final reservation/quotes
reservation[-1] = reservation_price(
    mid_price=s[-1],
    inventory=inventory[-1],
    gamma=gamma,
    sigma=sigma,
    time_remaining=0.0,
)

bid[-1], ask[-1] = optimal_quotes(
    reservation=reservation[-1],
    gamma=gamma,
    k=k,
)


# ============================================================
# Results
# ============================================================

print("Final inventory:", inventory[-1])
print("Final cash:", cash[-1])
print("Final mid-price:", s[-1])
print("Final P&L:", pnl[-1])


# ============================================================
# Plot
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 4))


# Price and quotes
axes[0].plot(t, s, label="Mid-price")
axes[0].plot(t, reservation, "--", label="Reservation price")
axes[0].plot(t, bid, ".", label="Bid")
axes[0].plot(t, ask, ".", label="Ask")

axes[0].set_xlabel("Time")
axes[0].set_ylabel("Price")
axes[0].set_title("Market-making quotes")
axes[0].legend()
axes[0].grid(True)


# P&L
axes[1].plot(t, pnl, label="P&L")

axes[1].set_xlabel("Time")
axes[1].set_ylabel("P&L")
axes[1].set_title("P&L")
axes[1].legend()
axes[1].grid(True)


# Inventory
axes[2].plot(t, inventory, label="Inventory")

axes[2].set_xlabel("Time")
axes[2].set_ylabel("Inventory")
axes[2].set_title("Inventory")
axes[2].legend()
axes[2].grid(True)


plt.tight_layout()
plt.show()