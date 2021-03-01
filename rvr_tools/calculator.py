#TODO MDF is wrong for postflop 3+bets - risk not reduced by initial bets and
#  initial bet not added to reward.
class MDF(object):
    """
    MDF Calculator Object

    Input:
    pot, bet, invest, villain_invest

    """

    def __init__(self,
                 pot: float,
                 bet: float,
                 invest: float = 0,
                 villain_invest: float = 0
                 ) -> None:
        self.pot = pot
        self.bet = bet
        self.invest = invest
        self.villain_invest = villain_invest

    def __repr__(self) -> str:
        return f"""MDF(pot={self.pot}, bet={self.bet}, invest={self.invest}
                , villain_invest={self.villain_invest})"""

    def __str__(self) -> str:
        return f"{self.mdf}"

    @property
    def mdf(self) -> float:
        return 1 - self.alpha

    @property
    def mdf_pct(self) -> float:
        return self.mdf * 100

    @property
    def alpha(self) -> float:
        return (self.bet / (self.bet
                            + self.pot
                            + self.invest
                            + self.villain_invest))

    @property
    def alpha_pct(self) -> float:
        return self.alpha * 100
