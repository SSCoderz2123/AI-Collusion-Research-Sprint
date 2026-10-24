"""Logit Bertrand duopoly (Calvano et al. 2020 calibration).

Demand for firm i:
    q_i = exp((a - p_i) / mu) / (sum_j exp((a - p_j) / mu) + exp(a0 / mu))

Profit for firm i: (p_i - c) * q_i.

Default parameters a=2, a0=0, mu=0.25, c=1 give a static Nash price of
about 1.473 and a joint-profit (monopoly) price of about 1.925.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass(frozen=True)
class MarketParams:
    a: float = 2.0
    a0: float = 0.0
    mu: float = 0.25
    cost: float = 1.0
    n_firms: int = 2


@dataclass
class Market:
    params: MarketParams = field(default_factory=MarketParams)

    def __post_init__(self) -> None:
        self.nash_price = self._solve_nash_price()
        self.monopoly_price = self._solve_monopoly_price()
        self.nash_profit = self.profits([self.nash_price] * self.params.n_firms)[0]
        self.monopoly_profit = self.profits([self.monopoly_price] * self.params.n_firms)[0]

    # ------------------------------------------------------------------ demand
    def quantities(self, prices: list[float]) -> list[float]:
        p = self.params
        # Subtract the largest exponent before exp() to prevent overflow.
        exps = [(p.a - price) / p.mu for price in prices] + [p.a0 / p.mu]
        top = max(exps)
        weights = [math.exp(e - top) for e in exps]
        total = sum(weights)
        return [w / total for w in weights[:-1]]

    def profits(self, prices: list[float]) -> list[float]:
        qs = self.quantities(prices)
        return [(price - self.params.cost) * q for price, q in zip(prices, qs, strict=True)]

    # ---------------------------------------------------------- best response
    def best_response(self, rival_prices: list[float]) -> float:
        """Static best response to fixed rival prices.

        The first-order condition of the logit model is (p - c)(1 - q(p)) = mu.
        The left side increases in p, so bisection finds the unique root.
        """
        c, mu = self.params.cost, self.params.mu

        def foc(price: float) -> float:
            q = self.quantities([price] + list(rival_prices))[0]
            return (price - c) * (1.0 - q) - mu

        lo, hi = c, c + 50.0 * mu
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if foc(mid) > 0:
                hi = mid
            else:
                lo = mid
        return 0.5 * (lo + hi)

    def _solve_nash_price(self) -> float:
        price = self.params.cost + self.params.mu
        for _ in range(500):
            new = self.best_response([price] * (self.params.n_firms - 1))
            if abs(new - price) < 1e-12:
                break
            price = new
        return price

    def _solve_monopoly_price(self) -> float:
        """Symmetric price that maximises joint profit (golden-section search)."""
        n = self.params.n_firms

        def joint(price: float) -> float:
            return sum(self.profits([price] * n))

        lo, hi = self.params.cost, self.params.cost + 50.0 * self.params.mu
        ratio = (math.sqrt(5) - 1) / 2
        x1, x2 = hi - ratio * (hi - lo), lo + ratio * (hi - lo)
        for _ in range(300):
            if joint(x1) < joint(x2):
                lo = x1
                x1, x2 = x2, lo + ratio * (hi - lo)
            else:
                hi = x2
                x2, x1 = x1, hi - ratio * (hi - lo)
        return 0.5 * (lo + hi)

    # ------------------------------------------------------------- indices
    def profit_index(self, profit: float) -> float:
        """Calvano Delta: 0 at the Nash profit, 1 at the monopoly profit."""
        return (profit - self.nash_profit) / (self.monopoly_profit - self.nash_profit)

    def price_index(self, price: float) -> float:
        """0 at the Nash price, 1 at the monopoly price."""
        return (price - self.nash_price) / (self.monopoly_price - self.nash_price)
