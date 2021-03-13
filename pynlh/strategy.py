from pynlh import Range


class StrategyError(Exception):
    pass

    def __init__(self, name: str, msg: str = 'Not a valid Strategy!'):
        """
        Exception class pf pynlh's Strategy class.
        """
        self.name = name
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"'{self.name}' -> {self.msg}"


class Strategy():

    def __init__(self,
                 name: str,
                 aggressive_ranges: Range,
                 passive_range: Range,
                 ) -> None:
        """
        Pynlh's Strategy class.
        This Class represents a complete strategy for a single spot. So a
        decision for every hand. It has a range for aggressive actions
        (bet/raise), one for the passive action (i.e. check or call) and one
        for folding.
        """
        self.name = name
        self.aggressive_ranges = aggressive_ranges
        self.passive_range = passive_range
