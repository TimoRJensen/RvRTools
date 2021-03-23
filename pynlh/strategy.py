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
                 aggressive_range: Range,
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
        self.aggressive_range = aggressive_range
        self.passive_range = passive_range
        self.folding_range = (Range.full_range()
                              - (aggressive_range + passive_range))

    def __contains__(self, key) -> bool:
        return (key in self.aggressive_range) or (key in self.passive_range)

    def _create_easiness_dict(self) -> dict:
        raise NotImplementedError
        rv = Range.build_0freq_hands_dict()
        xy_dict = Range.build_xy_dict()
        # print(xy_dict[(13, 3)])
        for hand, (rate, x, y) in rv.items():
            steps = 0
            next_x = x
            next_y = y
            next_hand = hand
            while next_hand in self:
                steps += 1
                next_x += 1
                next_y += 1
                if (next_x == 14) or (next_y == 14):
                    break
                next_hand = xy_dict[(next_x, next_y)]
            rv[hand] = (steps, x, y)
        return rv

    def _get_easiness(self, hand) -> int:
        raise NotImplementedError
        # xy_dict = Range.build_xy_dict()
        aggro = self.aggressive_range
        if hand in aggro:
            if hand in self.passive_range:
                return 1
            else:
                return self._count_steps_to_next_subrange(hand,
                                                          aggro)
        else:
            if hand in self.passive_range:
                return self._count_steps_to_next_subrange(hand,
                                                          self.passive_range)
            else:
                return self._count_steps_to_next_subrange(hand,
                                                          self.folding_range)

    def _count_steps_to_next_subrange(self, hand, range_) -> int:
        raise NotImplementedError
